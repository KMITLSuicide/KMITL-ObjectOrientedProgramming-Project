import ReactPlayer from "react-player"
import { type CourseLearnMaterialVideo } from "~/src/lib/definitions/course"

export function CourseLearnVideo ({
  videoData
  } : {
  videoData: CourseLearnMaterialVideo
}) {
  return (
    <>
      <div className="relative w-full max-h-[90%] h-full">
        <ReactPlayer
          url={videoData?.url}
          controls={true}
          width="100%"
          height="100%"
        />
      </div>
      <h1 className="my-8 text-3xl font-bold">{videoData?.name}</h1>
      <p>{videoData?.description}</p>
    </>
  );
}