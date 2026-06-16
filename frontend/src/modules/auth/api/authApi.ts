import request, { type PageResult } from "@/shared/api/request";
import type {
  CertificationPayload,
  CertificationStatus,
  CurrentUser,
  LoginPayload,
  LoginResult,
  ProfileUpdatePayload,
  PublicUser,
  RegisterPayload,
  RiskAssessmentPayload,
  RiskAssessmentResult,
  VerifyCodePayload
} from "../types/auth";

export function register(payload: RegisterPayload) {
  return request.post<{ userId: number }>("/auth/register", payload);
}

export function login(payload: LoginPayload) {
  return request.post<LoginResult>("/auth/login", payload);
}

export function logout() {
  return request.post<null>("/auth/logout");
}

export function sendVerifyCode(payload: VerifyCodePayload) {
  return request.post<{ message: string; code: string }>("/auth/verify-code", payload);
}

export function fetchCurrentUser() {
  return request.get<CurrentUser>("/users/me");
}

export function updateProfile(payload: ProfileUpdatePayload) {
  return request.put<null>("/users/me/profile", payload);
}

export function fetchPublicUser(id: number) {
  return request.get<PublicUser>(`/users/${id}`);
}

export function searchUsers(keyword: string, page = 1, size = 10) {
  return request.get<PageResult<PublicUser>>("/users/search", {
    params: { keyword, page, size }
  });
}

export function fetchCertificationStatus() {
  return request.get<CertificationStatus>("/users/me/certification");
}

export function submitCertification(payload: CertificationPayload) {
  return request.post<{ authLevel: number; message: string }>("/users/me/certification", payload);
}

export function submitRiskAssessment(payload: RiskAssessmentPayload) {
  return request.post<RiskAssessmentResult>("/users/me/risk-assessment", payload);
}
