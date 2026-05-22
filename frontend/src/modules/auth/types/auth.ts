export type AccountType = "phone" | "email";
export type CertificationType = "REAL_NAME" | "PROFESSIONAL";

export interface UserBrief {
  id: number;
  nickname: string;
  authLevel: number;
  role: string;
  status: number;
}

export interface CurrentUser extends UserBrief {
  phone?: string | null;
  email?: string | null;
  avatarUrl?: string | null;
  bio?: string | null;
  riskPreference?: number | null;
  influenceScore: number;
}

export interface PublicUser {
  id: number;
  nickname?: string | null;
  avatarUrl?: string | null;
  bio?: string | null;
  authLevel: number;
  influenceScore: number;
}

export interface RegisterPayload {
  accountType: AccountType;
  phone?: string;
  email?: string;
  password: string;
  nickname: string;
  verifyCode: string;
}

export interface LoginPayload {
  account: string;
  password: string;
}

export interface LoginResult {
  token: string;
  user: UserBrief;
}

export interface VerifyCodePayload {
  accountType: AccountType;
  target: string;
}

export interface ProfileUpdatePayload {
  nickname?: string;
  avatarUrl?: string;
  bio?: string;
  riskPreference?: number;
}

export interface CertificationPayload {
  certificationType: CertificationType;
  realName: string;
  materialUrls?: string[];
}

export interface CertificationStatus {
  authLevel: number;
  status: string;
}

export interface RiskAssessmentPayload {
  answers: number[];
}

export interface RiskAssessmentResult {
  riskPreference: number;
  label: string;
}
