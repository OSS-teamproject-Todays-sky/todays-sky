//영어 특보(event) → 한글 번역 테이블
export const ALERT_TRANSLATIONS: Record<string, string> = {
  "DryAir Advisory": "건조주의보",
  "Storm Surge Advisory": "폭풍해일주의보",
  "Heavy Rain Advisory": "호우주의보",
  "High Wind Advisory": "강풍주의보",
  "High Wave Advisory": "풍랑주의보",
  "Cold Wave Advisory": "한파주의보",
  "Heavy Snow Advisory": "대설주의보",
  "Yellow Dust Advisory": "황사주의보",
  "Typhoon Advisory": "태풍주의보",
  "Heatwave Advisory": "폭염주의보",
  "Tsunami Advisory": "해일주의보",
};

// 특보 텍스트 변환 함수
export const translateAlert = (event: string): string => {
  if (!event || event === "None") return "현재 발효된 특보가 없습니다";
  // 앞에 붙어 있는 "[기상특보]" 같은 패턴을 제거
  const cleaned = event.replace(/\[.*?\]\s*/g, "");

  return ALERT_TRANSLATIONS[cleaned] || cleaned;
};
