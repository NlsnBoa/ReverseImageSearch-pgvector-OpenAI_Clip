import AuthButton from "@/components/AuthButton";
import { createClient } from "@/utils/supabase/server";
import  Link  from "next/link";

export default async function Index() {
  const canInitSupabaseClient = () => {
    try {
      createClient();
      return true;
    } catch (e) {
      return false;
    }
  };
  
  const isSupabaseConnected = canInitSupabaseClient();

  const supabase = createClient();

  const {
    data: { user },
  } = await supabase.auth.getUser();

  return (
    <div className="flex-1 w-full flex flex-col gap-20 items-center">
      <nav className="w-full flex justify-center border-b border-b-foreground/10 h-16">
        <div className="w-full max-w-4xl flex justify-between items-center p-3 text-sm">
          <h1 className="w-fit mt-4 font-bold text-4xl mb-4">Whooga Image{" "} <span className=" text-green-500">Search Test</span></h1>
          {isSupabaseConnected && <AuthButton />}
        </div>
      </nav>

      <div className="animate-in flex-1 flex flex-col gap-20 opacity-0 max-w-4xl px-3">
        <main className="flex-1 flex flex-col gap-6">
          {user ? (
              <Link
              href="/search"
              className="py-2 px-3 flex rounded-md no-underline bg-btn-background hover:bg-btn-background-hover"
            >
              Click Me To Start Searching
            </Link>
          ):( 
            <h2 className="font-bold text-4xl mb-4 mx-auto">Sign in to start Searching</h2>
          )}
        </main>
      </div>

    </div>
  );
}
