import { redirect } from "next/navigation";

export default function NoCourseID() {
  redirect("/search");
}
