import 'package:flutter/material.dart';
import 'package:fyp_prototype/widgets/custom_app_bar.dart';

class ImportDatasetPage extends StatefulWidget {
  const ImportDatasetPage({super.key});

  @override
  State<ImportDatasetPage> createState() => _ImportDatasetPageState();
}

class _ImportDatasetPageState extends State<ImportDatasetPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: CustomAppBar(title: 'Import Dataset', subtitle: 'Upload your own weather or pest data')
    );
  }
}