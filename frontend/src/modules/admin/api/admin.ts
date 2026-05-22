import request from "@/shared/api/request";
import type {
  AdminStatistics,
  AdminOverview,
  AuditDecisionAction,
  AuditQueueItem,
  ReportDecisionAction,
  ReportItem,
  SensitiveWord,
  UserModerationRecord
} from "../types/admin";

export async function fetchOverview() {
  return request.get<AdminOverview>("/admin/overview");
}

export async function fetchAuditQueue() {
  return request.get<AuditQueueItem[]>("/admin/audit-queue");
}

export async function fetchReports() {
  return request.get<ReportItem[]>("/admin/reports");
}

export async function fetchSensitiveWords() {
  return request.get<SensitiveWord[]>("/admin/sensitive-words");
}

export async function updateAuditQueueItem(id: number, action: AuditDecisionAction) {
  return request.patch<AuditQueueItem>(`/admin/audit-queue/${id}`, { action });
}

export async function updateReportItem(id: number, action: ReportDecisionAction) {
  return request.patch<ReportItem>(`/admin/reports/${id}`, { action });
}

export async function toggleSensitiveWord(id: number, enabled: boolean) {
  return request.patch<SensitiveWord>(`/admin/sensitive-words/${id}`, { enabled });
}

export async function fetchUserModerationRecords() {
  return request.get<UserModerationRecord[]>("/admin/user-moderation");
}

export async function fetchAdminStatistics() {
  return request.get<AdminStatistics>("/admin/statistics");
}
