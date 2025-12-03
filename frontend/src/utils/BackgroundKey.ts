// 날씨 문자열(sky)을 정규화하여 스타일에서 사용할 key로 변환

export const BackgroundKey = (sky: string, isNight: boolean): string => {
  if (isNight) {
    // 구현되어 있는 밤 이미지 목록
    const nightAvailable = ["fog", "rain", "snow", "thunder"];

    if (sky.includes("흐림") || sky.includes("구름많음")) {
      return nightAvailable.includes("fog") ? "fog_night" : "__NO_NIGHT_IMAGE__";
    }
    if (sky.includes("비") || sky.includes("소나기") || sky.includes("이슬비")) {
      return nightAvailable.includes("rain") ? "rain_night" : "__NO_NIGHT_IMAGE__";
    }
    if (sky.includes("눈")) {
      return nightAvailable.includes("snow") ? "snow_night" : "__NO_NIGHT_IMAGE__";
    }
    if (sky.includes("뇌우")) {
      return nightAvailable.includes("thunder") ? "thunder_night" : "__NO_NIGHT_IMAGE__";
    }

    // "밤인데 맑음", clear_night 없음, StarryBackground 사용
    if (sky.includes("맑음")) {
      return "__NO_NIGHT_IMAGE__";
    }
    //밤인데 이미지가 없을경우, StarryBackground 사용
    return "__NO_NIGHT_IMAGE__";
  }

  // 낮
  if (sky.includes("맑음")) return "clear";
  if (sky.includes("구름많음") || sky.includes("흐림")) return "fog";
  if (sky.includes("비") || sky.includes("소나기") || sky.includes("이슬비")) return "rain";
  if (sky.includes("눈")) return "snow";

  //낮인데 이미지가 없을경우, StarryBackground 사용
  return "__NO_IMAGE__";
};