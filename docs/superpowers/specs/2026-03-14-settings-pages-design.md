# Settings Pages + Farm Management Fix — Design Spec

**Date:** 2026-03-14
**Scope:** 5 features across backend (FastAPI) and mobile (Flutter)

---

## 1. Edit Profile

### Problem
- "Edit Profile" button on settings page does nothing (TODO)
- No backend endpoint to update user profile
- No email field on User model — needed for new signups

### Backend Changes

**User model (`models/user.py`):**
- Add `email` column: `String(255)`, optional, unique, indexed

**Schemas (`schemas/auth.py`):**
- `UserUpdate` (new): all fields optional — `full_name`, `email`, `farm_location_name`, `farm_location_lat`, `farm_location_lng`, `crop_type`
- `PasswordChange` (new): `current_password` (required), `new_password` (required, min 6 chars)
- `UserRegister`: add `email` field (required for new signups)
- `UserResponse`: add `email` field

**Endpoints (`routers/auth.py`):**
- `PUT /api/v1/auth/me` — accepts `UserUpdate` body, updates current user's profile fields. Returns updated `UserResponse`. Returns 409 Conflict if email is already in use by another user.
- `POST /api/v1/auth/change-password` — accepts `PasswordChange` body, verifies `current_password` against stored hash, sets `new_password`. Returns 200 on success, 400 if current password wrong.

**User model `to_dict()` method:**
- Add `email` to the returned dictionary

**Migration:**
- Alembic migration to add `email` column (nullable for existing users)

### Mobile Changes

**User model (`models/user.dart`):**
- Add `email` field (String?, nullable)
- Update `fromJson` / `toJson`

**AuthService (`services/auth_service.dart`):**
- `updateProfile(Map<String, dynamic> fields)` → calls `PUT /api/v1/auth/me`
- `changePassword(String currentPassword, String newPassword)` → calls `POST /api/v1/auth/change-password`

**AuthProvider (`providers/auth_provider.dart`):**
- `updateProfile(...)` — calls service, refreshes user on success
- `changePassword(...)` — calls service, returns success/error

**API Constants (`utils/api_constants.dart`):**
- Add `profileUpdate` = `$apiPrefix/auth/me`
- Add `changePassword` = `$apiPrefix/auth/change-password`

**New page — `EditProfilePage` (`pages/edit_profile_page.dart`):**
- Full-page form using `CustomAppBar` with title "Edit Profile"
- Form fields (pre-populated from current user):
  - Full Name — text field
  - Email — text field with email keyboard type
  - Farm Location Name — text field
  - Farm Latitude — numeric text field
  - Farm Longitude — numeric text field
  - Crop Type — dropdown (rice, vegetables, corn, oil_palm, rubber)
- Save button with loading state and validation
- Separate section: "Change Password"
  - Current Password — obscured text field
  - New Password — obscured text field
  - Confirm New Password — obscured text field (UI-only validation, must match new password)
  - Change Password button
- Success/error feedback via SnackBar

**Registration screen:**
- Add email text field to registration form
- Pass email to register API call

**Routing (`main.dart`):**
- Add `/editProfile` → `EditProfilePage`

**Settings page (`pages/settings_page.dart`):**
- Wire "Edit Profile" button to `Navigator.pushNamed(context, '/editProfile')`

---

## 2. Import Dataset

### Problem
- Import Dataset page is an empty shell
- No backend endpoint for bulk sensor data import
- New users have empty accounts with no historical data

### Backend Changes

**Endpoint (`routers/sensor.py`):**
- `POST /api/v1/sensor/import` — accepts multipart file upload (CSV)
- Reads CSV (UTF-8 encoding, handles BOM), validates headers against known columns
- **Accepted CSV columns** (matching SensorReading model):
  - `temperature` (required — rows missing this are skipped)
  - `relative_humidity` (required — rows missing this are skipped). Alias: `humidity`
  - `soil_moisture` (required — rows missing this are skipped)
  - `rain` (default 0.0 if missing). Alias: `rainfall`
  - `wind_speed` (default 0.0 if missing)
  - `solar_radiation` (nullable, NULL if missing)
  - `soil_temperature` (nullable, NULL if missing)
  - `weather_code` (nullable, NULL if missing)
  - `timestamp` (if missing, uses current time; if present, parses ISO format or common date formats)
- Note: `temperature`, `relative_humidity`, and `soil_moisture` are NOT NULL in the database — rows missing these required columns are skipped with an error message
- Extra/unknown columns are silently ignored
- Each valid row creates a `SensorReading` record owned by the current user
- Returns JSON: `{ "rows_imported": int, "rows_skipped": int, "columns_matched": [str], "columns_missing": [str], "errors": [{"row": int, "message": str}] }`
- Limit: max 10,000 rows per import to prevent abuse
- Note: importing the same CSV twice will create duplicate rows (no deduplication)

### Mobile Changes

**pubspec.yaml:**
- Add `file_picker: ^8.0.0` dependency

**API Constants:**
- Add `sensorImport` = `$apiPrefix/sensor/import`

**Service:**
- Add `importSensorData(String filePath)` to sensor service or create dedicated import service
- Uses multipart POST request to upload CSV file

**Import Dataset page (`pages/import_dataset_page.dart`):**
- File picker button — filters to `.csv` files only
- After file selected:
  - Preview section showing first 5 rows in a horizontal-scrollable table
  - Column match summary: list of expected columns with green checkmark (matched) or grey dash (missing)
- Import button — shows progress indicator during upload
- Result summary after import:
  - Rows imported (green)
  - Rows skipped with error count (orange/red if any)
  - Option to view error details in expandable section
- Reset button to import another file

---

## 3. Help & Support

### Problem
- Page is an empty shell with just an AppBar

### Mobile Changes (no backend)

**pubspec.yaml:**
- Add `url_launcher: ^6.2.0` dependency

**Help & Support page (`pages/help_support_page.dart`):**
- Uses `CustomAppBar` with title "Help & Support", subtitle "FAQs and contact support"
- FAQ section — `ExpansionTile` list with hardcoded Q&As:
  1. "What is AgriSense?" — Brief app description
  2. "How does pest detection work?" — Upload image, AI analyzes, returns results
  3. "How do I set up farm sectors?" — Go to Farm Management in settings
  4. "What sensors are supported?" — Temperature, humidity, soil moisture, rainfall
  5. "How do I import historical data?" — Go to Import Dataset in settings
  6. "How does weather forecasting work?" — Uses Open-Meteo API, 5-day forecast
- Contact section at bottom:
  - "Contact Support" header
  - Email row — tappable, opens email client via `url_launcher`
  - GitHub row — tappable, opens repo in browser via `url_launcher`

---

## 4. About AgriSense

### Problem
- Page is an empty shell with just an AppBar

### Mobile Changes (no backend)

**About AgriSense page (`pages/about_agrisense_page.dart`):**
- Uses `CustomAppBar` with title "About AgriSense"
- Centered layout:
  - App icon/logo (from assets)
  - "AgriSense" title text
  - "Version 1.0.0" subtitle
  - Paragraph: "AgriSense is an IoT-driven agricultural monitoring system that helps farmers track environmental conditions, detect pests, and make data-driven decisions for their crops."
  - Divider
  - "Built with Flutter & FastAPI" footer text
  - Copyright line: "2026 AgriSense Team"

---

## 5. Farm Management Fix

### Problem
- Sector dialog has all free-text fields with no guidance or validation
- "Crop" should be a dropdown (backend has defined options)
- "Planted" should use a date picker, not free text
- "Area" is a string but backend has `area_value` (float) + `area_unit` (string)
- "Location" label is vague
- No form validation — empty name silently becomes "Unnamed Sector"
- Delete button shows for new sectors

### Mobile Changes (no backend changes needed)

**Sector model (`models/farm_sector.dart`):**
- Change `area` (String) → `areaValue` (double?) + `areaUnit` (String, default "acres")
- Update `fromJson` to read `area_value` and `area_unit` from backend
- Update `toJson` to send `area_value`, `area_unit`, and also `area` as `"${areaValue} ${areaUnit}"` for backward compatibility with the backend's legacy `area` string field
- Keep backward compatibility in `fromJson`: if backend sends `area` as string but no `area_value`, parse it

**Sector Dialog (`widgets/sector_dialog.dart.dart`):**
- **Name** — text field, required. Show validation error if empty on save.
- **Location** → relabel to "Plot Description", hint text: "e.g. North field, Block A"
- **Crop** → `DropdownButtonFormField` with options: Rice, Vegetables, Corn, Oil Palm, Rubber. If existing sector has a crop value not in the list, add it as a temporary option so it's not lost.
- **Area** → row with numeric `TextField` (decimal keyboard) + `DropdownButton` for unit (Acres, Hectares)
- **Planted** → read-only text field that opens `showDatePicker()` on tap. Displays formatted date.
- **Delete button** → only shown when editing existing sector (`initialSector != null && initialSector.id != null`)
- **Save validation** — name must not be empty; show error dialog or inline error if invalid

**Farm Sector Card (`widgets/farm_sector_card.dart`):**
- Update area display to show `"${areaValue} ${areaUnit}"` instead of raw string
- Handle null `areaValue` gracefully (show "Not set")

---

## Implementation Order

1. **Edit Profile** (backend + mobile) — foundation change, adds email to model
2. **Import Dataset** (backend + mobile) — requires backend endpoint
3. **Farm Management Fix** (mobile only) — UI improvements
4. **Help & Support** (mobile only) — static content
5. **About AgriSense** (mobile only) — static content

## Dependencies

- `file_picker` and `url_launcher` packages must be added to pubspec.yaml
- Alembic migration for email column must be applied before Edit Profile mobile work
- Registration screen email field should be done alongside the backend email changes
