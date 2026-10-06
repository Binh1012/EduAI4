package com.eduai4.app.data

import android.content.Context
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import com.eduai4.app.BuildConfig
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import okhttp3.OkHttpClient
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

private val Context.dataStore by preferencesDataStore("session")

/** Keeps the login token (DataStore) and mirrors it in memory for the HTTP interceptor. */
class SessionStore(private val ctx: Context) {
    private val tokenKey = stringPreferencesKey("token")
    private val nameKey = stringPreferencesKey("name")

    @Volatile var token: String? = null
        private set
    @Volatile var name: String = "bạn nhỏ"
        private set

    init {
        runBlocking {
            val p = ctx.dataStore.data.first()
            token = p[tokenKey]
            p[nameKey]?.let { name = it }
        }
    }

    suspend fun save(t: String, n: String) {
        token = t; name = n
        ctx.dataStore.edit { it[tokenKey] = t; it[nameKey] = n }
    }

    suspend fun clear() {
        token = null; name = "bạn nhỏ"
        ctx.dataStore.edit { it.clear() }
    }
}

/** Simple service locator (enough for this project size; swap for Hilt later if needed). */
object Graph {
    lateinit var session: SessionStore
        private set
    lateinit var repo: Repository
        private set

    fun init(ctx: Context) {
        session = SessionStore(ctx.applicationContext)
        val client = OkHttpClient.Builder().addInterceptor { chain ->
            val req = chain.request().newBuilder()
            session.token?.let { req.header("Authorization", "Bearer $it") }
            chain.proceed(req.build())
        }.build()
        val api = Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .client(client)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
        repo = Repository(api, session)
    }
}
