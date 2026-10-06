package com.eduai4.app.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.eduai4.app.viewmodel.AuthViewModel

@Composable
fun AuthScreen(vm: AuthViewModel) {
    var register by remember { mutableStateOf(false) }
    var name by remember { mutableStateOf("") }
    var email by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    val loading by vm.loading.collectAsState()
    val error by vm.error.collectAsState()

    Column(
        Modifier.fillMaxSize().verticalScroll(rememberScrollState()).padding(24.dp),
        Arrangement.Center, Alignment.CenterHorizontally,
    ) {
        Text("📚", fontSize = 64.sp)
        Text("EduAI 4", fontSize = 36.sp, fontWeight = FontWeight.ExtraBold)
        Text("Học thật vui cùng AI", fontSize = 18.sp)
        Spacer(Modifier.height(24.dp))
        if (register) {
            OutlinedTextField(name, { name = it }, label = { Text("Tên của em") }, singleLine = true, modifier = Modifier.fillMaxWidth())
            Spacer(Modifier.height(8.dp))
        }
        OutlinedTextField(
            email, { email = it }, label = { Text("Email") }, singleLine = true,
            keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Email), modifier = Modifier.fillMaxWidth(),
        )
        Spacer(Modifier.height(8.dp))
        OutlinedTextField(
            password, { password = it }, label = { Text("Mật khẩu (từ 6 ký tự)") }, singleLine = true,
            visualTransformation = PasswordVisualTransformation(), modifier = Modifier.fillMaxWidth(),
        )
        error?.let {
            Spacer(Modifier.height(8.dp))
            Text("💡 $it", color = Bad, textAlign = TextAlign.Center)
        }
        Spacer(Modifier.height(16.dp))
        val ready = email.isNotBlank() && password.length >= 6 && (!register || name.isNotBlank())
        BigButton(
            if (loading) "Đang xử lý..." else if (register) "Đăng ký" else "Đăng nhập",
            onClick = { if (register) vm.register(name, email, password) else vm.login(email, password) },
            enabled = ready && !loading,
        )
        TextButton(onClick = { register = !register; vm.clearError() }) {
            Text(if (register) "Đã có tài khoản? Đăng nhập" else "Chưa có tài khoản? Đăng ký", fontSize = 16.sp)
        }
    }
}
