import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/main.dart';
import 'package:flutter/material.dart';

void main() {
  testWidgets('Dashboard displays correctly', (WidgetTester tester) async {
    // Simulate a desktop window.
    tester.view.physicalSize = const Size(1600, 1000);
    tester.view.devicePixelRatio = 1.0;

    await tester.pumpWidget(const DeviationApp());

    expect(find.text('Deviation Tracker'), findsOneWidget);
    expect(find.text('Dashboard'), findsNWidgets(2));
    expect(find.text('Total Deviations'), findsOneWidget);
    expect(find.text('Analytics'), findsOneWidget);

    // Reset the test window.
    addTearDown(tester.view.resetPhysicalSize);
    addTearDown(tester.view.resetDevicePixelRatio);
  });
}