import { getSupportedCities } from "@/features/home/api";
import { HomePage } from "@/features/home/HomePage";

export default async function Page() {
  const cities = await getSupportedCities();

  return <HomePage cities={cities} />;
}
