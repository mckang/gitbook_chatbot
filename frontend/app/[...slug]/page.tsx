"use client";

type Props = {
    params: {
      slug: string[];
    };
  };

export default function DynamicPage({ params }: Props) {
    // params.slug를 사용하여 페이지 내용 결정
    return <div>Dynamic Page for {params.slug.join('/')}</div>;
}