"use client";

import { FormEvent, useId, useState } from "react";
import { supabase } from "./supabaseClient";

type AuthDialogProps = {
  isOpen: boolean;
  onAuthenticated: () => void;
  onClose: () => void;
};

export function AuthDialog({ isOpen, onAuthenticated, onClose }: AuthDialogProps) {
  const emailInputId = useId();
  const tokenInputId = useId();
  const [email, setEmail] = useState("");
  const [token, setToken] = useState("");
  const [isCodeSent, setIsCodeSent] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [status, setStatus] = useState<string | null>(null);

  if (!isOpen) {
    return null;
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    const trimmedEmail = email.trim();
    if (!trimmedEmail) {
      setStatus("请输入邮箱。");
      return;
    }

    setIsSubmitting(true);
    setStatus(null);

    try {
      if (!isCodeSent) {
        const { error } = await supabase.auth.signInWithOtp({
          email: trimmedEmail,
          options: {
            shouldCreateUser: true,
          },
        });

        if (error) {
          throw error;
        }

        setIsCodeSent(true);
        setStatus("验证码已发送，请查看邮箱。");
        return;
      }

      const trimmedToken = token.trim();
      if (!trimmedToken) {
        setStatus("请输入邮箱验证码。");
        return;
      }

      const { error } = await supabase.auth.verifyOtp({
        email: trimmedEmail,
        token: trimmedToken,
        type: "email",
      });

      if (error) {
        throw error;
      }

      setStatus("登录成功。");
      onAuthenticated();
    } catch {
      setStatus("登录暂时没有成功，请检查邮箱或稍后重试。");
    } finally {
      setIsSubmitting(false);
    }
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

          {isCodeSent && (
            <div className="space-y-2">
              <label className="text-sm font-medium text-neutral-800" htmlFor={tokenInputId}>
                邮箱验证码
              </label>
              <input
                className="min-h-12 w-full rounded-xl border border-neutral-300 px-3 text-base outline-none transition focus:border-neutral-950"
                id={tokenInputId}
                inputMode="numeric"
                disabled={isSubmitting}
                onChange={(event) => setToken(event.target.value)}
                placeholder="输入邮箱中的验证码"
                value={token}
              />
            </div>
          )}

          {status && <p className="text-sm leading-6 text-neutral-600">{status}</p>}

          <button
            className="min-h-12 w-full rounded-xl bg-neutral-950 px-4 text-sm font-medium text-white"
            disabled={isSubmitting}
            type="submit"
          >
            {isCodeSent ? "验证并继续" : "发送验证码"}
          </button>
        </form>
      </div>
    </div>
  );
}
