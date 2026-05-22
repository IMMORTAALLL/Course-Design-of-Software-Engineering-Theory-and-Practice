export type AdminOverview = {
  today_posts: number;
  pending_audits: number;
  pending_reports: number;
  active_sensitive_words: number;
};

export type AuditQueueItem = {
  id: number;
  content_type: string;
  title: string;
  author_name: string;
  reason: string;
  risk_level: string;
  status: string;
  created_at: string;
};

export type AuditDecisionAction = "approve" | "reject";

export type ReportItem = {
  id: number;
  target_type: string;
  target_title: string;
  reporter_name: string;
  reason: string;
  status: string;
  created_at: string;
};

export type ReportDecisionAction = "dismissed" | "warning_issued" | "banned";

export type SensitiveWord = {
  id: number;
  keyword: string;
  category: string;
  risk_level: string;
  action: string;
  enabled: boolean;
  note?: string | null;
  created_at: string;
};

export type UserModerationRecord = {
  id: number;
  user_name: string;
  action: string;
  reason: string;
  status: string;
  created_at: string;
};

export type AdminStatistics = {
  hot_topics: string[];
  active_sections: Array<{
    name: string;
    value: number;
  }>;
};
