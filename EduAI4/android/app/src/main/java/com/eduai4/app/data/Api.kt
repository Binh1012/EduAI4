package com.eduai4.app.data

import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path
import retrofit2.http.Query

interface ApiService {
    @POST("auth/login") suspend fun login(@Body body: LoginReq): TokenRes
    @POST("auth/register") suspend fun register(@Body body: RegisterReq): TokenRes
    @GET("subjects") suspend fun subjects(): List<SubjectDto>
    @GET("topics/{id}/questions") suspend fun questions(@Path("id") id: Int, @Query("limit") limit: Int): List<QuestionDto>
    @POST("quiz/submit") suspend fun submit(@Body body: SubmitReq): ResultDto
    @GET("progress") suspend fun progress(): ProgressDto
    @GET("recommendations") suspend fun recommendations(): RecommendDto
    @POST("ai/tutor") suspend fun tutor(@Body body: TutorReq): TutorRes
}
