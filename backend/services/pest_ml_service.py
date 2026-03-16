"""
Pest ML Service - YOLOv5-based pest detection

Singleton service that loads a YOLOv5 model at startup and provides
inference for pest detection endpoints. Falls back to mock predictions
when the model file is missing or USE_MOCK_ML is enabled.

The model is loaded via torch.hub (ultralytics/yolov5) since the
trained weights are in YOLOv5 format.
"""

import logging
import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class Detection:
    """A single detected object from the YOLO model."""
    class_name: str
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]


@dataclass
class PestPredictionResult:
    """Structured result from pest inference."""
    pest_type: Optional[str]       # Highest-confidence class name
    confidence: float              # 0.0-1.0
    all_detections: List[Detection] = field(default_factory=list)
    model_loaded: bool = False     # True = real model, False = mock


class PestMLService:
    """Singleton YOLOv5 pest detection service."""

    def __init__(self):
        self._model = None
        self._class_names: Dict[int, str] = {}
        self._model_loaded = False

    # ------------------------------------------------------------------
    # Model lifecycle
    # ------------------------------------------------------------------

    def load_model(self, model_path: str) -> bool:
        """Load a YOLOv5 .pt model file via torch.hub. Returns True on success."""
        path = Path(model_path)
        if not path.exists():
            logger.warning("Pest model not found at %s - using mock predictions", path)
            return False

        try:
            import sys
            import os
            import torch

            # torch.hub.load downloads YOLOv5 repo to cache, then imports from it.
            # Our /app/models/ package shadows YOLOv5's models/ module.
            # Fix: temporarily chdir to the hub repo so relative imports resolve there.
            hub_dir = os.path.join(
                os.environ.get("TORCH_HOME", os.path.expanduser("~/.cache/torch")),
                "hub", "ultralytics_yolov5_master"
            )

            original_cwd = os.getcwd()
            original_path = sys.path.copy()

            try:
                # Ensure hub repo is downloaded
                if not os.path.isdir(hub_dir):
                    torch.hub.load("ultralytics/yolov5", "custom",
                                   path=str(path), trust_repo=True)
                else:
                    # Insert hub dir at front and remove /app so YOLOv5's
                    # models/ is found before our backend models/
                    os.chdir(hub_dir)
                    sys.path.insert(0, hub_dir)
                    sys.path = [p for p in sys.path if p not in ("/app",)]

                    model_abs_path = str(path) if path.is_absolute() else str(Path(original_cwd) / path)
                    self._model = torch.hub.load(
                        hub_dir,
                        "custom",
                        path=model_abs_path,
                        source="local",
                        trust_repo=True,
                    )
            finally:
                os.chdir(original_cwd)
                sys.path = original_path
            self._model.conf = 0.25  # default confidence threshold
            self._class_names = self._model.names  # {0: "name", ...}
            self._model_loaded = True
            logger.info(
                "Pest ML model loaded from %s - classes: %s",
                path, list(self._class_names.values()),
            )
            return True
        except Exception:
            logger.exception("Failed to load pest ML model from %s", path)
            self._model = None
            self._model_loaded = False
            return False

    @property
    def is_loaded(self) -> bool:
        return self._model_loaded

    @property
    def class_names(self) -> Dict[int, str]:
        return dict(self._class_names)

    # ------------------------------------------------------------------
    # Inference
    # ------------------------------------------------------------------

    def predict(self, image_path: str, conf_threshold: float = 0.25) -> PestPredictionResult:
        """
        Run YOLOv5 inference on an image.

        If the model is not loaded, returns a mock prediction.
        YOLOv5 results expose a pandas DataFrame via results.pandas().xyxy[0].

        Args:
            image_path: Path to the image file.
            conf_threshold: Minimum confidence for detections (default 0.25).

        Returns:
            PestPredictionResult with the primary detection + all detections.
        """
        if not self._model_loaded or self._model is None:
            return self._mock_predict()

        try:
            self._model.conf = conf_threshold
            results = self._model(image_path)

            # YOLOv5 results: results.xyxy[0] is a tensor [x1, y1, x2, y2, conf, cls]
            preds = results.xyxy[0]  # tensor on CPU

            if preds is None or len(preds) == 0:
                return PestPredictionResult(
                    pest_type=None,
                    confidence=0.0,
                    all_detections=[],
                    model_loaded=True,
                )

            detections: List[Detection] = []
            for row in preds:
                x1, y1, x2, y2, conf, cls_id = row.tolist()
                class_name = self._class_names.get(int(cls_id), f"class_{int(cls_id)}")
                detections.append(Detection(
                    class_name=class_name,
                    confidence=round(conf, 4),
                    bbox=[round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1)],
                ))

            # Sort by confidence descending
            detections.sort(key=lambda d: d.confidence, reverse=True)
            primary = detections[0]

            return PestPredictionResult(
                pest_type=primary.class_name,
                confidence=round(primary.confidence, 4),
                all_detections=detections,
                model_loaded=True,
            )

        except Exception:
            logger.exception("YOLOv5 inference failed for %s", image_path)
            return self._mock_predict()

    # ------------------------------------------------------------------
    # Mock fallback
    # ------------------------------------------------------------------

    @staticmethod
    def _mock_predict() -> PestPredictionResult:
        """Return a random mock prediction (dev/testing fallback)."""
        mock_pests = [
            "Rice Stem Borer",
            "Rice Leaf Folder",
            "Brown Planthopper",
            "Rice Bug",
            "Green Leafhopper",
        ]
        pest = random.choice(mock_pests)
        conf = round(random.uniform(0.3, 0.95), 2)

        return PestPredictionResult(
            pest_type=pest,
            confidence=conf,
            all_detections=[Detection(
                class_name=pest,
                confidence=conf,
                bbox=[0.0, 0.0, 100.0, 100.0],
            )],
            model_loaded=False,
        )


# Module-level singleton
pest_ml_service = PestMLService()
