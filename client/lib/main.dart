import 'package:material_ui/material_ui.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Ascend',
      theme: ThemeData(colorScheme: .fromSeed(seedColor: Colors.green)),
      home: const MyHomePage(title: 'Welcome to ASCEND'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});
  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  bool _showQuestionMark = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        title: Text(widget.title),
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          crossAxisAlignment: .center,
          children: [
            Text(
              'Do you want to change your life?',
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            Text(
              "Since you're here, it's no longer a question.",
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            Text(
              "How long will you be strong? ",
              style: Theme.of(context).textTheme.headlineMedium,
            ),
            SizedBox(width: 50),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                TweenAnimationBuilder<double>(
                  tween: Tween(begin: 0, end: 30),
                  duration: const Duration(seconds: 3),
                  builder: (context, value, child) {
                    return Text(
                      _showQuestionMark ? '?' : value.round().toString(),
                      style: Theme.of(context).textTheme.headlineMedium,
                    );
                  },
                  onEnd: () {
                    setState(() {
                      _showQuestionMark = true;
                    });
                  },
                ),
                Text(
                  " days",
                  style: Theme.of(context).textTheme.headlineMedium,
                ),
              ],
            ),
            SizedBox(width: 50),
            AuthSegmentedButton(),
          ],
        ),
      ),
    );
  }
}

class AuthSegmentedButton extends StatefulWidget {
  const AuthSegmentedButton({super.key});

  @override
  State<AuthSegmentedButton> createState() => _AuthSegmentedButton();
}

enum Auth { login, register }

class _AuthSegmentedButton extends State<AuthSegmentedButton> {
  Auth menuView = .login;

  @override
  Widget build(BuildContext context) {
    return SegmentedButton<Auth>(
      style: SegmentedButton.styleFrom(
        backgroundColor: Colors.grey,
        foregroundColor: Colors.red,
        selectedForegroundColor: Colors.white,
        selectedBackgroundColor: Colors.green,
      ),
      segments: const <ButtonSegment<Auth>>[
        ButtonSegment<Auth>(
          value: Auth.login,
          label: Text("Authentication"),
          icon: Icon(Icons.login),
        ),
        ButtonSegment<Auth>(
          value: Auth.register,
          label: Text("Registration"),
          icon: Icon(Icons.app_registration),
        ),
      ],
      selected: <Auth>{menuView},
      onSelectionChanged: (Set<Auth> newSelection) {
        setState(() {
          menuView = newSelection.first;
        });
      },
    );
  }
}
