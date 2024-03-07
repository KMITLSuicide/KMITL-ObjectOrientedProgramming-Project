'use client';

import { type AppRouterInstance } from "next/dist/shared/lib/app-router-context.shared-runtime";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { CourseCard } from "~/src/components/course/card";
import { Card, CardHeader, CardTitle } from "~/src/components/ui/card";

import { searchCategory, searchCourse, searchTeacher } from "~/src/lib/data/search";
import { type CourseCardData } from "~/src/lib/definitions/course";
import { type SearchResults } from "~/src/lib/definitions/search";

function createGenericCards(searchResults: SearchResults[] | null | undefined, urlPrefix: string | undefined, router: AppRouterInstance) {
  return searchResults?.map((result) => {
    return (
      <Card
        className="w-full cursor-pointer hover:bg-secondary "
        key={result.id}
      >
        <Link href={`/${urlPrefix}/${result.id}`}>
          <CardHeader>
            <CardTitle>{result.name}</CardTitle>
          </CardHeader>
        </Link>
      </Card>
    );
  })
}

export default function SearchResults({ params }: { params: { type: string, query: string }}) {
  const router = useRouter();
  const [searchResults, setSearchResults] = useState<SearchResults[] | CourseCardData[] | null | undefined>(undefined);
  const [urlPrefix, setUrlPrefix] = useState<string | undefined>(undefined);
  const [cards, setCards] = useState<JSX.Element[] | undefined>(undefined);

  useEffect(() => {
    async function fetchData(type: string) {
      if (params.type === "course") {
        return await searchCourse(type)
      } else if (params.type === "category") {
        return await searchCategory(type)
      } else if (params.type === "teacher") {
        return await searchTeacher(type)
      }
    }

    void fetchData(params.query).then((data) => {
      setSearchResults(data);
      setUrlPrefix(params.type);
    });
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (params.type === "course") {
      setCards((searchResults as CourseCardData[]).map((course) => <CourseCard course={course} key={course.id} />) ?? []);
    } else {
      setCards(createGenericCards(searchResults, urlPrefix, router) ?? []);
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchResults]);

  return (
    <div className="flex justify-center w-full">
      <div className="w-full max-w-screen-lg space-y-4">
        <h2 className="font-semibold text-xl">Searching by {params.type}</h2>
        <h1 className="font-bold text-2xl">Search results for {params.query}</h1>
        <div className="grid grid-cols-4 gap-4">
          {cards?.map((card) => card)}
        </div>
      </div>
    </div>
    // <code>
    //   {JSON.stringify(searchResults, null, 2)}
    // </code>
  );
}