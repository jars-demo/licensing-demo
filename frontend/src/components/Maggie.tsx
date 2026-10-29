// Maggie the magpie, drawn in flat shapes: a black head and back, the white belly and shoulder
// patch, a blue-and-teal sheen on the wing and a long tail. `face` crops to the head for the
// round button.

export function Maggie({ className = '', face = false }: { className?: string; face?: boolean }) {
  return (
    <svg
      viewBox={face ? '2 10 32 32' : '0 0 64 64'}
      className={className}
      role="img"
      aria-label="Maggie the magpie"
    >
      <g className="maggie-tail">
        <path d="M40 42 62 58l-4 3-21-13z" fill="#141414" />
        <path d="M45 46l14 11" stroke="#2ec4b6" strokeWidth="1.8" />
      </g>
      <ellipse cx="34" cy="40" rx="15" ry="12" fill="#141414" />
      <ellipse cx="29" cy="44" rx="10" ry="7.5" fill="#f7f6f1" />
      <path d="M33 31c8 0 13 4 15 10-6 2-12 1-16-3z" fill="#f7f6f1" />
      <path d="M37 40c5 1 9 3 11 6-5 1-10 0-13-3z" fill="#3a5bd9" />
      <path d="M37 40c5 1 9 3 11 6" stroke="#2ec4b6" strokeWidth="1.4" fill="none" />
      <path d="M30 51v7M36 51v7" stroke="#3a3936" strokeWidth="1.6" strokeLinecap="round" />
      <circle cx="22" cy="25" r="11" fill="#141414" />
      <circle cx="19" cy="22" r="2.6" fill="#f7f6f1" />
      <circle cx="18.6" cy="22" r="1.3" fill="#141414" />
      <path d="M12 25 3 28l9 2z" fill="#3a3936" />
    </svg>
  )
}
