import { CityPage } from "@/features/city/CityPage";
import { getCityRecommendations } from "@/features/city/api";

type PageProps = {
  params: Promise<{
    slug: string;
  }>;
};

export default async function Page({ params }: PageProps) {
  const { slug } = await params;
  const recommendations = await getCityRecommendations(slug);

  return <CityPage recommendations={recommendations} />;
}
