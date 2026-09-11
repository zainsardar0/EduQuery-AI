import { useState } from 'react'
import { Eye, EyeOff } from 'lucide-react'

/**
 * Floating-label input shared by the login form. `peer` + `:not(:placeholder-shown)`
 * detects "has content" without extra state — the field only needs one of
 * value/onChange, which the parent already owns for validation.
 */
export function FloatingField({
  id,
  label,
  type = 'text',
  value,
  onChange,
  error,
  autoComplete,
  ...props
}) {
  const [reveal, setReveal] = useState(false)
  const isPassword = type === 'password'
  const inputType = isPassword ? (reveal ? 'text' : 'password') : type

  return (
    <div>
      <div className="relative">
        <input
          id={id}
          type={inputType}
          value={value}
          onChange={onChange}
          placeholder=" "
          autoComplete={autoComplete}
          aria-invalid={error ? 'true' : undefined}
          aria-describedby={error ? `${id}-error` : undefined}
          className={`peer w-full rounded-xl border bg-surface px-4 pt-6 pb-2.5 text-[0.9375rem] text-ink outline-none transition-colors duration-200 ${
            isPassword ? 'pr-12' : ''
          } ${
            error
              ? 'border-alert focus:border-alert focus:ring-4 focus:ring-alert/15'
              : 'border-line-2 focus:border-accent-sky-deep focus:ring-4 focus:ring-accent-sky-deep/15'
          }`}
          {...props}
        />
        <label
          htmlFor={id}
          className="pointer-events-none absolute top-4 left-4 text-[0.9375rem] text-ink-3 transition-all duration-200 peer-focus:top-2.5 peer-focus:text-xs peer-focus:text-accent-sky-deep peer-[&:not(:placeholder-shown)]:top-2.5 peer-[&:not(:placeholder-shown)]:text-xs"
        >
          {label}
        </label>
        {isPassword && (
          <button
            type="button"
            onClick={() => setReveal((v) => !v)}
            aria-label={reveal ? 'Hide password' : 'Show password'}
            className="absolute top-1/2 right-3.5 flex h-8 w-8 -translate-y-1/2 cursor-pointer items-center justify-center rounded-full text-ink-3 transition-colors hover:bg-surface-2 hover:text-ink"
          >
            {reveal ? <EyeOff size={16} strokeWidth={2} /> : <Eye size={16} strokeWidth={2} />}
          </button>
        )}
      </div>
      {error && (
        <p id={`${id}-error`} className="mt-1.5 pl-1 text-xs font-medium text-alert">
          {error}
        </p>
      )}
    </div>
  )
}
