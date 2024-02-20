import {
    Avatar,
    AvatarFallback,
    AvatarImage,
} from "~/src/components/ui/avatar";

export default function AvatarDemo() {
    return (
        <Avatar>
            <AvatarImage src="/default_avatar.png" alt="Profile picture" />
            <AvatarFallback>PY</AvatarFallback>
        </Avatar>
    );
}
