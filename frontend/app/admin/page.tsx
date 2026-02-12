"use client";

import { useEffect, useState } from "react";
import { useAuth } from "@clerk/nextjs";

type OptionDetail = {
  id: number;
  value: string;
};

type Reservation = {
  id: number;
  resource_name: string;
  user_email: string;
  user_first_name: string;
  user_last_name: string;
  status: string;
  created_at: string;
  selected_options_details: OptionDetail[];
};

export default function AdminPage() {
  const { getToken } = useAuth();

  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminReservations();
  }, []);

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

  // 🔥 UPDATE STATUS
  const updateStatus = async (id: number, newStatus: string) => {
    const token = await getToken({ template: "django" });

    const res = await fetch(
      `http://127.0.0.1:8000/api/admin-reservations/${id}/update-status/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({ status: newStatus }),
      }
    );

    if (!res.ok) {
      alert("Erreur lors de la mise à jour");
      return;
    }

    // 🔄 Mise à jour locale immédiate (sans reload)
    setReservations((prev) =>
      prev.map((r) =>
        r.id === id ? { ...r, status: newStatus } : r
      )
    );
  };

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
          {/* USER */}
          <p className="text-lg font-semibold">
            👤 {res.user_first_name || "Prénom inconnu"}{" "}
            {res.user_last_name || ""}
          </p>

          <p className="text-sm text-gray-500 mb-3">
            📧 {res.user_email || "Email inconnu"}
          </p>

          {/* PRODUCT */}
          <p>
            🕯️ <strong>Produit :</strong> {res.resource_name}
          </p>

          {/* OPTIONS */}
          {res.selected_options_details &&
            res.selected_options_details.length > 0 && (
              <div className="mt-2">
                🎨 <strong>Options :</strong>
                <ul className="list-disc list-inside text-sm mt-1 text-gray-600 dark:text-gray-400">
                  {res.selected_options_details.map((opt) => (
                    <li key={opt.id}>{opt.value}</li>
                  ))}
                </ul>
              </div>
            )}

          {/* STATUS */}
          <p className="mt-3">
            📌 <strong>Status :</strong>{" "}
            <span className="font-semibold">{res.status}</span>
          </p>

          {/* 🔥 ACTION BUTTONS */}
          <div className="flex gap-3 mt-4">
            {res.status !== "confirmed" && (
              <button
                onClick={() => updateStatus(res.id, "confirmed")}
                className="px-4 py-2 bg-green-600 text-white rounded-lg"
              >
                ✅ Confirmer
              </button>
            )}

            {res.status !== "cancelled" && (
              <button
                onClick={() => updateStatus(res.id, "cancelled")}
                className="px-4 py-2 bg-red-600 text-white rounded-lg"
              >
                ❌ Annuler
              </button>
            )}
          </div>

          {/* DATE */}
          <p className="text-sm text-gray-500 mt-4">
            🗓️ {new Date(res.created_at).toLocaleString()}
          </p>
        </div>
      ))}
    </div>
  );
}