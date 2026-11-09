
import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

void main() {
  runApp(const DeviationApp());
}

class DeviationApp extends StatelessWidget {
  const DeviationApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Deviation Dashboard',
      theme: ThemeData(
        useMaterial3: true,
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF16805A),
        ),
        scaffoldBackgroundColor: const Color(0xFFF5F7F6),
      ),
      home: const DashboardPage(),
    );
  }
}

class DashboardPage extends StatefulWidget {
  const DashboardPage({super.key});

  @override
  State<DashboardPage> createState() => _DashboardPageState();
}

class _DashboardPageState extends State<DashboardPage> {
  int selectedIndex = 0;

  final List<String> menuItems = [
    'Dashboard',
    'Deviations',
    'Analytics',
    'Settings',
  ];

  final List<IconData> menuIcons = [
    Icons.dashboard_outlined,
    Icons.assignment_outlined,
    Icons.analytics_outlined,
    Icons.settings_outlined,
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Row(
        children: [
          // LEFT SIDEBAR
          Container(
            width: 230,
            color: const Color(0xFF14532D),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Padding(
                  padding: EdgeInsets.all(24),
                  child: Text(
                    'Deviation Tracker',
                    style: TextStyle(
                      color: Colors.white,
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),

                const Divider(color: Colors.white24),

                const SizedBox(height: 12),

                // NAVIGATION MENU
                ...List.generate(menuItems.length, (index) {
                  final isSelected = selectedIndex == index;

                  return InkWell(
                    onTap: () {
                      setState(() {
                        selectedIndex = index;
                      });
                    },
                    child: Container(
                      margin: const EdgeInsets.symmetric(
                        horizontal: 12,
                        vertical: 4,
                      ),
                      padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 14,
                      ),
                      decoration: BoxDecoration(
                        color: isSelected
                            ? Colors.white.withValues(alpha: 0.16)
                            : Colors.transparent,
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Row(
                        children: [
                          Icon(
                            menuIcons[index],
                            color: Colors.white,
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child:Text(
                              menuItems[index],
                              overflow: TextOverflow.ellipsis,
                              style: const TextStyle(
                                color: Colors.white,
                                fontSize: 15,
                              ),
                            ),
                          )
                        ],
                      ),
                    ),
                  );
                }),

                const Spacer(),

                const Padding(
                  padding: EdgeInsets.all(20),
                  child: Text(
                    'Deviation Tracker v1.0',
                    style: TextStyle(
                      color: Colors.white70,
                      fontSize: 12,
                    ),
                  ),
                ),
              ],
            ),
          ),

          // MAIN CONTENT
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                // TOP HEADER
                Container(
                  height: 75,
                  color: Colors.white,
                  padding: const EdgeInsets.symmetric(horizontal: 30),
                  child: Row(
                    children: [
                      Text(
                        menuItems[selectedIndex],
                        style: const TextStyle(
                          fontSize: 23,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const Spacer(),
                      const Icon(
                        Icons.account_circle_outlined,
                        size: 30,
                        color: Color(0xFF14532D),
                      ),
                      const SizedBox(width: 10),
                      const Text('Administrator'),
                    ],
                  ),
                ),

                // PAGE CONTENT
                Expanded(
                  child: Padding(
                    padding: const EdgeInsets.all(30),
                    child: selectedIndex == 0
                        ? buildDashboard()
                        : Center(
                            child: Text(
                              '${menuItems[selectedIndex]} page coming soon',
                              style: const TextStyle(fontSize: 22),
                            ),
                          ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  // DASHBOARD CONTENT
  Widget buildDashboard() {
    return SingleChildScrollView(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Overview',
            style: TextStyle(
              fontSize: 24,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 8),

          const Text(
            'Monitor and manage project deviations.',
            style: TextStyle(
              color: Colors.grey,
              fontSize: 14,
            ),
          ),

          const SizedBox(height: 25),

          // KPI CARDS
          Wrap(
            spacing: 20,
            runSpacing: 20,
            children: [
              buildKpiCard(
                'Total Deviations',
                '30',
                Icons.assignment_outlined,
                const Color(0xFF16805A),
              ),
              buildKpiCard(
                'Open',
                '8',
                Icons.pending_actions,
                Colors.orange,
              ),
              buildKpiCard(
                'In Progress',
                '8',
                Icons.sync,
                Colors.blue,
              ),
              buildKpiCard(
                'Closed',
                '14',
                Icons.check_circle_outline,
                Colors.green,
              ),
            ],
          ),

          const SizedBox(height: 30),

          // ANALYTICS CHARTS
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: buildChartCard(
                  'Deviations by Type',
                  buildTypeChart(),
                ),
              ),
              const SizedBox(width: 20),
              Expanded(
                child: buildChartCard(
                  'Deviations by Status',
                  buildStatusChart(),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  // REUSABLE KPI CARD
  Widget buildKpiCard(
    String title,
    String value,
    IconData icon,
    Color color,
  ) {
    return Container(
      width: 210,
      height: 125,
      padding: const EdgeInsets.all(18),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Row(
            children: [
              Expanded(
                child:Text(
                title,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: const TextStyle(
                  color: Colors.grey,
                  fontSize: 13,
                  ),
                ),
              ),
              const SizedBox(width: 8),
              Icon(icon, color: color),
            ],
          ),
          Text(
            value,
            style: const TextStyle(
              fontSize: 28,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
  
Widget buildChartCard(String title, Widget chart) {
  return Container(
    height: 350,
    padding: const EdgeInsets.all(20),
    decoration: BoxDecoration(
      color: Colors.white,
      borderRadius: BorderRadius.circular(12),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          title,
          style: const TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
          ),
        ),
        const SizedBox(height: 25),
        Expanded(child: chart),
      ],
    ),
  );
}

Widget buildTypeChart() {
  final values = [7.0, 6.0, 6.0, 6.0, 5.0];

  return BarChart(
    BarChartData(
      maxY: 8,
      barGroups: List.generate(values.length, (index) {
        return BarChartGroupData(
          x: index,
          barRods: [
            BarChartRodData(
              toY: values[index],
              color: const Color(0xFF16805A),
              width: 24,
              borderRadius: BorderRadius.circular(4),
            ),
          ],
        );
      }),
      titlesData: FlTitlesData(
        topTitles: const AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
        rightTitles: const AxisTitles(
          sideTitles: SideTitles(showTitles: false),
        ),
        bottomTitles: AxisTitles(
          sideTitles: SideTitles(
            showTitles: true,
            getTitlesWidget: (value, meta) {
              const labels = [
                'Safety',
                'Install.',
                'Quality',
                'Material',
                'Other',
              ];

              final index = value.toInt();

              if (index < 0 || index >= labels.length) {
                return const SizedBox();
              }

              return SideTitleWidget(
                meta: meta,
                child: Text(
                  labels[index],
                  style: const TextStyle(fontSize: 10),
                ),
              );
            },
          ),
        ),
      ),
      borderData: FlBorderData(show: false),
      gridData: const FlGridData(show: false),
    ),
  );
}

  Widget buildStatusChart() {
    return PieChart(
      PieChartData(
        centerSpaceRadius: 45,
        sectionsSpace: 4,
        sections: [
          PieChartSectionData(
            value: 8,
            title: 'Open\n8',
            color: Colors.orange,
            radius: 65,
            titleStyle: const TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
              fontSize: 12,
            ),
          ),
          PieChartSectionData(
            value: 8,
            title: 'In Progress\n8',
            color: Colors.blue,
            radius: 65,
            titleStyle: const TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
              fontSize: 11,
            ),
          ),
          PieChartSectionData(
            value: 14,
            title: 'Closed\n14',
            color: Colors.green,
            radius: 65,
            titleStyle: const TextStyle(
              color: Colors.white,
              fontWeight: FontWeight.bold,
              fontSize: 12,
            ),
          ),
        ],
      ),
    );
  }
}