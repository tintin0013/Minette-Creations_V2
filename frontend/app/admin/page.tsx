"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@clerk/nextjs";

type Reservation = {
  id: number;
  resource_name: string;
  user_email: string;
  user_first_name: string;
  user_last_name: string;
  status: string;
  created_at: string;
};

export default function AdminPage() {
  const { getToken } = useAuth();

  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAdminReservations = async () => {
      const token = await getToken({ template: "django" });

      const res = await fetch(
        "http://127.0.0.1:8000/api/admin-reservations/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (!res.ok) {
        alert("Accès refusé (pas admin)");
        setLoading(false);
        return;
      }

      const data = await res.json();
      setReservations(data);
      setLoading(false);
    };

    fetchAdminReservations();
  }, []);

  if (loading) {
    return <div className="p-10">Chargement...</div>;
  }

  return (
    <div className="min-h-screen p-10 bg-zinc-50 dark:bg-black">
      <h1 className="text-3xl font-bold mb-8">🛠️ Interface Admin</h1>

      {reservations.length === 0 && (
        <p>Aucune réservation trouvée.</p>
      )}

      {reservations.map((res) => (
        <div
          key={res.id}
          className="p-6 mb-6 border rounded-xl bg-white dark:bg-zinc-900 shadow"
        >
          <p className="text-lg font-semibold">
            👤 {res.user_first_name} {res.user_last_name}
          </p>

          <p className="text-sm text-gray-500 mb-2">
            📧 {res.user_email}
          </p>

          <p>
            🕯️ <strong>Produit :</strong> {res.resource_name}
          </p>

          <p>
            📌 <strong>Status :</strong> {res.status}
          </p>

          <p className="text-sm text-gray-500">
            🗓️ {new Date(res.created_at).toLocaleString()}
          </p>
        </div>
      ))}
    </div>
  );
}