"use client";

import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  UserButton,
  useAuth,
} from "@clerk/nextjs";
import { useEffect, useState } from "react";

type Category = {
  id: number;
  name: string;
  slug: string;
};

type Resource = {
  id: number;
  name: string;
  description: string;
  photos: {
    id: number;
    image_url: string;
    position: number;
  }[];
};

export default function Home() {
  const { getToken } = useAuth();

  const [response, setResponse] = useState<any>(null);

  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const [resources, setResources] = useState<Resource[]>([]);
  const [loadingResources, setLoadingResources] = useState(false);

  const [loadingCategories, setLoadingCategories] = useState(true);
  const [errorCategories, setErrorCategories] = useState<string | null>(null);

  // 🔹 Test API protégée
  const callBackend = async () => {
    const token = await getToken();

    const res = await fetch("http://127.0.0.1:8000/api/protected/", {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    const data = await res.json();
    setResponse(data);
  };

  // 🔹 Chargement catégories
  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await fetch("http://127.0.0.1:8000/api/categories/");
        if (!res.ok) throw new Error("Erreur API");

        const data = await res.json();
        setCategories(data);
      } catch {
        setErrorCategories("Impossible de charger les catégories");
      } finally {
        setLoadingCategories(false);
      }
    };

    fetchCategories();
  }, []);

  // 🔹 Chargement ressources quand catégorie sélectionnée
  useEffect(() => {
    if (!selectedCategory) return;

    const fetchResources = async () => {
      setLoadingResources(true);

      const res = await fetch(
        `http://127.0.0.1:8000/api/resources/?category=${selectedCategory}`
      );

      const data = await res.json();
      setResources(data);
      setLoadingResources(false);
    };

    fetchResources();
  }, [selectedCategory]);

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-black flex justify-center">
      <main className="w-full max-w-4xl p-10 space-y-10">
        <h1 className="text-3xl font-bold text-center text-black dark:text-white">
          Minette Creations V2
        </h1>

        {/* 🔹 Catégories */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Catégories</h2>

          {loadingCategories && <p>Chargement...</p>}
          {errorCategories && <p className="text-red-500">{errorCategories}</p>}

          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {categories.map((cat) => (
              <div
                key={cat.id}
                onClick={() => setSelectedCategory(cat.slug)}
                className={`p-4 border rounded-lg cursor-pointer transition ${
                  selectedCategory === cat.slug
                    ? "bg-black text-white"
                    : "hover:bg-gray-100"
                }`}
              >
                {cat.name}
              </div>
            ))}
          </div>
        </div>

        {/* 🔹 Ressources */}
        {selectedCategory && (
          <div>
            <h2 className="text-xl font-semibold mb-4">
              Produits : {selectedCategory}
            </h2>

            {loadingResources && <p>Chargement produits...</p>}

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {resources.map((res) => (
                <div
                  key={res.id}
                  className="border rounded-lg overflow-hidden shadow-sm"
                >
                  {res.photos.length > 0 && (
                    <img
                      src={res.photos[0].image_url}
                      alt={res.name}
                      className="w-full h-48 object-cover"
                    />
                  )}

                  <div className="p-4">
                    <h3 className="font-bold text-lg">{res.name}</h3>
                    <p className="text-sm text-gray-600">
                      {res.description}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 🔐 Auth */}
        <SignedOut>
          <div className="flex justify-center gap-4">
            <SignInButton mode="modal">
              <button className="px-6 py-2 bg-black text-white rounded-lg">
                Se connecter
              </button>
            </SignInButton>

            <SignUpButton mode="modal">
              <button className="px-6 py-2 border border-black rounded-lg hover:bg-black hover:text-white">
                Créer un compte
              </button>
            </SignUpButton>
          </div>
        </SignedOut>

        <SignedIn>
          <div className="flex flex-col items-center gap-4">
            <p>Vous êtes connecté ✅</p>
            <UserButton afterSignOutUrl="/" />

            <button
              onClick={callBackend}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg"
            >
              Tester API backend
            </button>

            {response && (
              <pre className="mt-4 p-4 bg-gray-100 text-sm rounded-lg max-w-md overflow-auto">
                {JSON.stringify(response, null, 2)}
              </pre>
            )}
          </div>
        </SignedIn>
      </main>
    </div>
  );
}