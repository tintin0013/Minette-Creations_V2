"use client";

import {
  SignedIn,
  SignedOut,
  SignInButton,
  SignUpButton,
  useAuth,
  useClerk,
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

type Reservation = {
  id: number;
  resource: {
    id: number;
    name: string;
  };
  created_at: string;
};

export default function Home() {
  const { getToken } = useAuth();
  const { signOut } = useClerk();

  const [categories, setCategories] = useState<Category[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);
  const [resources, setResources] = useState<Resource[]>([]);
  const [reservations, setReservations] = useState<Reservation[]>([]);

  const [isAdmin, setIsAdmin] = useState(false);

  const [loadingCategories, setLoadingCategories] = useState(true);
  const [loadingReservations, setLoadingReservations] = useState(false);

  // ==========================
  // 🔹 CHECK ADMIN STATUS
  // ==========================

  const checkAdminStatus = async () => {
    const token = await getToken({ template: "django" });

    if (!token) return;

    const res = await fetch("http://127.0.0.1:8000/api/protected/", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });

    if (!res.ok) return;

    const data = await res.json();
    setIsAdmin(data.is_admin);
  };

  // 🔹 Quand user connecté → on vérifie son rôle
  useEffect(() => {
    checkAdminStatus();
  }, []);

  // ==========================
  // 🔹 Catégories
  // ==========================

  useEffect(() => {
    const fetchCategories = async () => {
      const res = await fetch("http://127.0.0.1:8000/api/categories/");
      const data = await res.json();
      setCategories(data);
      setLoadingCategories(false);
    };

    fetchCategories();
  }, []);

  // ==========================
  // 🔹 Mes réservations
  // ==========================

  const fetchMyReservations = async () => {
    setLoadingReservations(true);

    const token = await getToken({ template: "django" });

    const res = await fetch(
      "http://127.0.0.1:8000/api/my-reservations/",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await res.json();
    setReservations(data);
    setLoadingReservations(false);
  };

  // ==========================
  // 🔥 Logout propre
  // ==========================

  const handleLogout = async () => {
    await signOut({ redirectUrl: "/" });
  };

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-black flex justify-center">
      <main className="w-full max-w-5xl p-10 space-y-10">
        <h1 className="text-3xl font-bold text-center">
          Minette Creations V2
        </h1>

        {/* 🔐 AUTH */}
        <SignedOut>
          <div className="flex justify-center gap-4">
            <SignInButton mode="modal">
              <button className="px-6 py-2 bg-black text-white rounded-lg">
                Se connecter
              </button>
            </SignInButton>

            <SignUpButton mode="modal">
              <button className="px-6 py-2 border border-black rounded-lg">
                Créer un compte
              </button>
            </SignUpButton>
          </div>
        </SignedOut>

        <SignedIn>
          <div className="flex flex-col items-center gap-4">
            <p>Vous êtes connecté ✅</p>

            {/* 🔥 BOUTON ADMIN (VISIBLE UNIQUEMENT SI ADMIN) */}
            {isAdmin && (
              <button
                className="px-6 py-2 bg-purple-600 text-white rounded-lg"
                onClick={async () => {
                  const token = await getToken({ template: "django" });
                  const res = await fetch(
                    "http://127.0.0.1:8000/api/admin-reservations/",
                    {
                      headers: {
                        Authorization: `Bearer ${token}`,
                      },
                    }
                  );
                  const data = await res.json();
                  console.log("ADMIN DATA:", data);
                  alert("Données admin affichées dans la console");
                }}
              >
                🛠️ Interface Admin
              </button>
            )}

            <button
              onClick={fetchMyReservations}
              className="px-6 py-2 bg-green-600 text-white rounded-lg"
            >
              Voir mes réservations
            </button>

            {loadingReservations && <p>Chargement...</p>}

            {reservations.map((res) => (
              <div key={res.id}>
                {res.resource.name} —{" "}
                {new Date(res.created_at).toLocaleString()}
              </div>
            ))}

            <button
              onClick={handleLogout}
              className="px-6 py-2 bg-red-600 text-white rounded-lg"
            >
              Se déconnecter
            </button>
          </div>
        </SignedIn>
      </main>
    </div>
  );
}