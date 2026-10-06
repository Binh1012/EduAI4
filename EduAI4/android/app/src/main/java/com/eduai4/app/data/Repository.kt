package com.eduai4.app.data

import com.google.gson.Gson
import java.io.IOException
import kotlinx.coroutines.CancellationException
import retrofit2.HttpException

private data class ErrorBody(val detail: String?)

/** Single entry point to the backend. Every call returns Result with a child-friendly Vietnamese message. */
class Repository(private val api: ApiService, private val session: SessionStore) {

    private suspend fun <T> call(block: suspend () -> T): Result<T> = try {
        Result.success(block())
    } catch (e: CancellationException) {
        throw e
    } catch (e: HttpException) {
        Result.failure(Exception(httpMessage(e)))
    } catch (e: IOException) {
        Result.failure(Exception("Không kết nối được máy chủ. Hãy kiểm tra mạng rồi thử lại."))
    } catch (e: Exception) {
        Result.failure(Exception("Có lỗi xảy ra. Hãy thử lại."))
    }

    private fun httpMessage(e: HttpException): String {
        if (e.code() == 422) return "Thông tin chưa hợp lệ. Kiểm tra email và mật khẩu (từ 6 ký tự)."
        val body = e.response()?.errorBody()?.string()
        val detail = try { Gson().fromJson(body, ErrorBody::class.java)?.detail } catch (_: Exception) { null }
        return detail ?: "Lỗi máy chủ (${e.code()})."
    }

    suspend fun login(email: String, password: String): Result<Unit> = call {
        val r = api.login(LoginReq(email, password)); session.save(r.access_token, r.name)
    }

    suspend fun register(name: String, email: String, password: String): Result<Unit> = call {
        val r = api.register(RegisterReq(email, name, password)); session.save(r.access_token, r.name)
    }

    suspend fun logout() = session.clear()

    suspend fun subjects() = call { api.subjects() }
    suspend fun questions(topicId: Int) = call { api.questions(topicId, 10) }
    suspend fun submit(req: SubmitReq) = call { api.submit(req) }
    suspend fun progress() = call { api.progress() }
    suspend fun recommend() = call { api.recommendations() }
    suspend fun tutor(question: String) = call { api.tutor(TutorReq(question)).answer }
}
