import { getPlaceDetail } from "@/features/places/api";
import { PlaceDetailPage } from "@/features/places/PlaceDetailPage";

type PageProps = {
  params: Promise<{
    slug: string;
  }>;
};

export default async function Page({ params }: PageProps) {
  const { slug } = await params;
  const detail = await getPlaceDetail(slug);

  return <PlaceDetailPage detail={detail} />;
}
