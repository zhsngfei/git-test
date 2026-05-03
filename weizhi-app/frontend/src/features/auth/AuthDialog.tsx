"use client";

import { FormEvent, useId, useState } from "react";

export type SimulatedUser = {
  email: string;
  userId: string;
};

type AuthDialogProps = {
  isOpen: boolean;
  onAuthenticated: (user: SimulatedUser) => void;
  onClose: () => void;
};

export function AuthDialog({ isOpen, onAuthenticated, onClose }: AuthDialogProps) {
  const emailInputId = useId();
  const [email, setEmail] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  if (!isOpen) {
    return null;
  }

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedEmail = email.trim();
    if (!trimmedEmail) {
      setStatus("请输入邮箱。");
      return;
    }

    setIsSubmitting(true);
    const user = {
      email: trimmedEmail,
      userId: `local-${trimmedEmail.toLowerCase()}`,
    };

    setStatus("已记录你的邮箱，本阶段会先在当前设备保留收藏状态。");
    window.setTimeout(() => onAuthenticated(user), 450);
  }

  return (
    <div
      aria-labelledby="auth-dialog-title"
      aria-modal="true"
      className="fixed inset-0 z-50 flex items-end bg-neutral-950/40 px-4 pb-4 sm:items-center sm:justify-center sm:pb-0"
      role="dialog"
    >
      <div className="w-full max-w-md rounded-2xl bg-white p-5 shadow-xl">
        <div className="flex items-start justify-between gap-4">
          <div className="space-y-1">
            <h2 className="text-lg font-semibold text-neutral-950" id="auth-dialog-title">
              登录后收藏
            </h2>
            <p className="text-sm leading-6 text-neutral-600">输入邮箱即可继续当前收藏动作。</p>
          </div>
          <button
            aria-label="关闭登录弹窗"
            className="grid size-9 place-items-center rounded-full bg-neutral-100 text-xl leading-none text-neutral-600"
            onClick={onClose}
            type="button"
          >
            ×
          </button>
        </div>

        <form className="mt-5 space-y-4" onSubmit={handleSubmit}>
          <div className="space-y-2">
            <label className="text-sm font-medium text-neutral-800" htmlFor={emailInputId}>
              邮箱
            </label>
            <input
              className="min-h-12 w-full rounded-xl border border-neutral-300 px-3 text-base outline-none transition focus:border-neutral-950"
              id={emailInputId}
              inputMode="email"
              disabled={isSubmitting}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@example.com"
              type="email"
              value={email}
            />
          </div>

          {status && <p className="text-sm leading-6 text-neutral-600">{status}</p>}

          <button
            className="min-h-12 w-full rounded-xl bg-neutral-950 px-4 text-sm font-medium text-white"
            disabled={isSubmitting}
            type="submit"
          >
            继续收藏
          </button>
        </form>
      </div>
    </div>
  );
}
