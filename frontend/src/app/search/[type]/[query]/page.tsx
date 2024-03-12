"use client";
export const runtime = 'edge';

import Link from "next/link";
import { useEffect, useState } from "react";
import { CourseCard } from "~/src/components/course/card";
import { Card, CardHeader, CardTitle } from "~/src/components/ui/card";
import { toast } from "~/src/components/ui/use-toast";

import {
  searchCategory,
  searchCourse,
  searchTeacher,
} from "~/src/lib/data/search";
import { type CourseCardData } from "~/src/lib/definitions/course";
import { type SearchResults } from "~/src/lib/definitions/search";

function createGenericCards(
  searchResults: SearchResults[] | null | undefined,
  urlPrefix: string | undefined,
) {
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
  });
}

export default function SearchResults({
  params,
}: {
  params: { type: string; query: string };
}) {
  const [searchResults, setSearchResults] = useState<
    SearchResults[] | CourseCardData[] | null | undefined
  >(undefined);
  const [urlPrefix, setUrlPrefix] = useState<string | undefined>(undefined);
  const [cards, setCards] = useState<JSX.Element[] | undefined>(undefined);

  useEffect(() => {
    async function fetchData(type: string) {
      if (params.type === "course") {
        return await searchCourse(type);
      } else if (params.type === "category") {
        return await searchCategory(type);
      } else if (params.type === "teacher") {
        return await searchTeacher(type);
      }
    }

    void fetchData(params.query).then((data) => {
      setSearchResults(data);
      setUrlPrefix(params.type);
      if (data === null) {
        toast({
          title: "Error",
          description: "Failed to fetch data",
          variant: "destructive",
        })}
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    if (searchResults !== undefined) {
      if (params.type === "course") {
        setCards(
          (searchResults as CourseCardData[]).map((course) => (
            <CourseCard course={course} key={course.id} showPrice showReviewScore />
          )) ?? [],
        );
      } else {
        setCards(createGenericCards(searchResults, urlPrefix) ?? []);
      }
    } else {
      setCards(undefined);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [searchResults]);

  return (
    <div className="flex w-full justify-center">
      <div className="w-full max-w-screen-lg space-y-4">
        <h2 className="text-xl font-semibold">Searching by {params.type}</h2>
        <h1 className="text-2xl font-bold">
          Search results for {params.query}
        </h1>
        <div className="grid grid-cols-4 gap-4">
          {cards?.map((card) => card)}
          {cards === undefined && <p>Loading...</p>}
          {cards?.length === 0 && <p>No results found</p>}
        </div>
      </div>
    </div>
  );
}
