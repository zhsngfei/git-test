import { getWorkDetail } from "@/features/works/api";
import { WorkDetailPage } from "@/features/works/WorkDetailPage";

type PageProps = {
  params: Promise<{
    slug: string;
  }>;
};

export default async function Page({ params }: PageProps) {
  const { slug } = await params;
  const detail = await getWorkDetail(slug);

  return <WorkDetailPage detail={detail} />;
}
