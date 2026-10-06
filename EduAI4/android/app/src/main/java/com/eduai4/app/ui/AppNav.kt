package com.eduai4.app.ui

import androidx.compose.foundation.layout.padding
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.eduai4.app.viewmodel.AuthViewModel
import com.eduai4.app.viewmodel.MainViewModel
import com.eduai4.app.viewmodel.TutorViewModel

private val tabs = listOf(
    Triple("home", "🏠", "Trang chủ"),
    Triple("progress", "📊", "Tiến độ"),
    Triple("tutor", "🤖", "Hỏi cô"),
)

@Composable
fun AppNav() {
    val nav = rememberNavController()
    val auth: AuthViewModel = viewModel()
    val main: MainViewModel = viewModel()
    val tutor: TutorViewModel = viewModel()
    val loggedIn by auth.loggedIn.collectAsState()
    val route = nav.currentBackStackEntryAsState().value?.destination?.route

    // React to login / logout
    LaunchedEffect(loggedIn) {
        val current = nav.currentDestination?.route
        if (!loggedIn && current != "login") {
            main.clear()
            nav.navigate("login") { popUpTo(0) { inclusive = true } }
        } else if (loggedIn && current == "login") {
            nav.navigate("home") { popUpTo("login") { inclusive = true } }
        }
    }

    Scaffold(
        bottomBar = {
            if (route in tabs.map { it.first }) {
                NavigationBar {
                    tabs.forEach { (r, icon, label) ->
                        NavigationBarItem(
                            selected = route == r,
                            onClick = {
                                nav.navigate(r) {
                                    popUpTo("home"); launchSingleTop = true
                                }
                            },
                            icon = { Text(icon) },
                            label = { Text(label) },
                        )
                    }
                }
            }
        },
    ) { inner ->
        NavHost(nav, startDestination = if (loggedIn) "home" else "login", modifier = Modifier.padding(inner)) {
            composable("login") { AuthScreen(auth) }
            composable("home") {
                HomeScreen(main, onSubject = { nav.navigate("subject/$it") }, onTopic = { nav.navigate("quiz/$it") })
            }
            composable("subject/{id}", arguments = listOf(navArgument("id") { type = NavType.IntType })) {
                SubjectScreen(main, it.arguments!!.getInt("id"), onBack = { nav.popBackStack() }, onTopic = { t -> nav.navigate("quiz/$t") })
            }
            composable("quiz/{id}", arguments = listOf(navArgument("id") { type = NavType.IntType })) {
                QuizScreen(it.arguments!!.getInt("id"), onExit = { nav.popBackStack("home", false) })
            }
            composable("progress") { ProgressScreen(main, onTopic = { nav.navigate("quiz/$it") }, onLogout = { auth.logout() }) }
            composable("tutor") { TutorScreen(tutor) }
        }
    }
}
