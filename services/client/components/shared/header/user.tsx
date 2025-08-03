import Logout from "@/components/logout";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import Image from "next/image";
import Link from "next/link";

type Props = {
  image?: string | null;
  name?: string | null;
  accountUrl: string;
};
async function User({ image, name, accountUrl }: Props) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          size={"lg"}
          variant={"outline"}
          className="relative py-5 pr-12 rounded-full flex items-center justify-between"
        >
          <span>{name}</span>
          <span className="absolute right-1 inline-block size-8 bg-red-500 rounded-full">
            {image && name && (
              <Image
                src={image}
                alt={name}
                width={32}
                height={32}
                className="rounded-full"
              />
            )}
          </span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent>
        <DropdownMenuLabel>My Account</DropdownMenuLabel>
        <DropdownMenuSeparator />
        <DropdownMenuItem asChild>
          <Link href={accountUrl}>Profile</Link>
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem asChild>
          <Logout />
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

export default User;
