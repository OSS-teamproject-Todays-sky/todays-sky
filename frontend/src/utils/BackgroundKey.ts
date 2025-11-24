// 날씨 문자열(sky)을 정규화하여 스타일에서 사용할 key로 변환

export const BackgroundKey = (sky: string): string => {
  if (sky === "맑음") return "clear";
  if (sky === "흐림" || sky === "구름많음") return "fog";
  if (sky === "비" || sky === "소나기" || sky === "이슬비") return "rain";
  if (sky === "눈") return "snow";
  if (sky === "뇌우") return "thunder";

  //어떠한 조건에도 맞지 않을경우 이미지가 없다고 가정하여 기본 배경 반환
  return "__NO_IMAGE__";
};