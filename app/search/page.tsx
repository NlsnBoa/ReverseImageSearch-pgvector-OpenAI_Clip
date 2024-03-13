import { createClient } from "@/utils/supabase/server";
import { redirect } from "next/navigation";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { ChooseFileButton } from "@/components/ChooseFileButton";
import AuthButton from "@/components/AuthButton";
import Header from "@/components/Header";

export default async function ProtectedPage() {
  const supabase = createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  if (!user) {
    return redirect("/login");
  }

  return (
    <div className="flex-1 w-full flex flex-col gap-20 items-center">
      <div className="w-full">
        <nav className="w-full flex justify-center border-b border-b-foreground/10 h-16">
          <div className="w-full max-w-4xl flex justify-between items-center p-3 text-sm">
            <h1 className="w-fit mt-4 font-bold text-4xl mb-4">
              Whooga Image <span className=" text-green-500">Search Test</span>
            </h1>
            <AuthButton />
          </div>
        </nav>
      </div>
      <Header></Header>
      <div className="animate-in flex-1 flex flex-col gap-20 opacity-0 max-w-4xl px-3">
        <main className="flex-1 flex flex-col gap-6">
          <h2 className="font-bold text-4xl mb-4 mx-auto">Search by Text</h2>
          <Input type="text" placeholder="Path Tag"></Input>
          <div className="w-full p-[1px] bg-gradient-to-r from-transparent via-foreground/10 to-transparent my-8" />
          <h2 className="font-bold text-4xl mx-auto">Search by Image</h2>
          <div className="grid w-full max-w-sm items-center gap-1.5">
            <Label htmlFor="picture">Upload your image</Label>
            <ChooseFileButton id="picture" type="file" />
          </div>
        </main>
      </div>
    </div>
  );
}
