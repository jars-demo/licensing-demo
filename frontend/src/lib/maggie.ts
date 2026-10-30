// Maggie, the magpie who collects shiny things and always asks whose they were. For each page: a
// short note and two quiz questions, each with one right answer and the reason it is right.

export type Question = {
  q: string
  options: readonly string[]
  answer: number
  why: string
}

export type Notes = { note: string; quiz: readonly Question[] }

const HOME: Notes = {
  note: 'I am Maggie. Magpies pick up anything shiny, which is how most projects collect code, fonts and logos. I keep the papers for everything I take. Try the explorer on this page: pick what you found and where you want to put it.',
  quiz: [
    {
      q: 'A public GitHub repository has no license file. What may you do with its code?',
      options: [
        'Anything: it is public',
        'View it, and fork it on GitHub',
        'Use it in non-commercial projects',
      ],
      answer: 1,
      why: "Copyright is automatic, so the default is all rights reserved. GitHub's terms let people view and fork public repositories on GitHub, and nothing more.",
    },
    {
      q: 'You copy one MIT-licensed file into your Apache-2.0 project. What do you keep?',
      options: [
        'Nothing, MIT has no conditions',
        "The file's copyright line and the MIT text",
        'You must relicense your project as MIT',
      ],
      answer: 1,
      why: "MIT's one condition is that its copyright notice and permission notice go with every copy. Your project keeps its own license.",
    },
  ],
}

const WORKSHOP: Notes = {
  note: 'Eight chapters, each a mistake I have seen in real repositories. The first three are about your own license, the next three about what you borrow, and the last two about what you ship. Each takes 15 to 20 minutes.',
  quiz: [
    {
      q: 'Which of these does a license scanner read?',
      options: ['The README', 'The manifest, such as package.json', 'The commit messages'],
      answer: 1,
      why: 'Scanners read the license field in each manifest. That is why a wrong value there matters even when LICENSE is right.',
    },
    {
      q: 'Who can change the license of a piece of code?',
      options: ['Anyone who forks it', 'Whoever hosts it', 'Its copyright owner'],
      answer: 2,
      why: 'Only the owner can relicense. Everyone else gets the license the owner chose, with its conditions.',
    },
  ],
}

const CHAPTERS: Record<string, Notes> = {
  '01': {
    note: '"Use it however you like" in a README is a kind thought and a legal shrug. A license says exactly what people may do. Fetch the canonical text, fill in the copyright line, and change nothing else.',
    quiz: [
      {
        q: 'You add one extra sentence to the MIT text. Is it still the MIT license?',
        options: [
          'Yes, MIT is flexible',
          'No, it is a new license nobody has reviewed',
          'Only if the sentence is short',
        ],
        answer: 1,
        why: 'Tools and lawyers recognise a license by its exact words. A changed MIT is a custom license, and every user has to read it from scratch.',
      },
      {
        q: 'What goes in `Copyright (c) [year] [fullname]`?',
        options: [
          'The year of first publication and the owner',
          'Today\'s date and "the authors"',
          'Leave the placeholders, they are standard',
        ],
        answer: 0,
        why: 'The line names who owns the code and since when. Placeholders left in mean nobody is named.',
      },
    ],
  },
  '02': {
    note: 'LICENSE is the law, the README tells people, the manifests tell machines. When they disagree, everyone stops. And watch npm: it writes ISC into every new package.json.',
    quiz: [
      {
        q: 'Which is a valid SPDX identifier?',
        options: ['MIT License', 'Apache 2', 'Apache-2.0'],
        answer: 2,
        why: 'SPDX ids are exact strings from a standard list. Tools match them character for character.',
      },
      {
        q: 'LICENSE is Apache-2.0 and the README says MIT. What should you change?',
        options: ['LICENSE, to match the README', 'The README, to match LICENSE', 'Neither'],
        answer: 1,
        why: 'The license file is what the author actually granted. The README describes it, so the README is the one that is wrong.',
      },
    ],
  },
  '03': {
    note: "Starting from a template is like borrowing a nest. You can redecorate, but the builder's name stays carved in it. Add your line under theirs.",
    quiz: [
      {
        q: 'You forked an MIT project. Whose copyright lines go in your LICENSE?',
        options: ['Only yours', 'Only theirs', 'Theirs, and yours for your changes'],
        answer: 2,
        why: 'Their code is still in your fork, so their notice must stay. Your changes are yours, so your line goes in too.',
      },
      {
        q: 'Does "based on kestrel-template" in the README meet MIT\'s condition?',
        options: [
          'Yes, it is a credit',
          'No, the notice and license text must ship',
          'Only on GitHub',
        ],
        answer: 1,
        why: 'MIT asks for the copyright notice and the permission notice in every copy. A friendly credit is neither.',
      },
    ],
  },
  '04': {
    note: 'Apache-2.0 is generous and tidy. It asks for four things: the license, the notices, a line saying what you changed, and the upstream NOTICE lines. Miss one and the permission does not hold.',
    quiz: [
      {
        q: 'You changed a file you copied from an Apache-2.0 project. What must the file say?',
        options: ['Nothing new', 'That you changed it', 'That it is now under your license'],
        answer: 1,
        why: 'Section 4(b): modified files must carry a prominent notice that you changed them.',
      },
      {
        q: 'Why can Apache-2.0 code not go into a GPL-2.0-only project?',
        options: [
          'Apache is not open source',
          'Its patent terms are restrictions GPL-2.0 forbids',
          'It can, there is no problem',
        ],
        answer: 1,
        why: 'GPL-2.0 forbids adding restrictions, and the Apache patent termination clause counts as one. GPL-3.0 was written to allow it.',
      },
    ],
  },
  '05': {
    note: 'I love shiny fonts. Each one comes with papers: the OFL travels with the font, and an icon set keeps its notice just like code does.',
    quiz: [
      {
        q: 'What does the SIL Open Font License not allow?',
        options: [
          'Bundling the font in a commercial app',
          'Selling the font on its own',
          'Embedding it in a PDF',
        ],
        answer: 1,
        why: 'The OFL allows almost any use, including commercial software. It forbids selling the font by itself.',
      },
      {
        q: 'An icon pack is free to download. Is that a license?',
        options: ['Yes', 'No, find its actual license', 'Only for personal use'],
        answer: 1,
        why: '"Free" describes the price, not the permission. Look for the license file before using it.',
      },
    ],
  },
  '06': {
    note: 'A logo file can be under an open license while the mark it shows is not. Say what you work with, never who backs you.',
    quiz: [
      {
        q: 'Which wording is safe?',
        options: ['Official Driftwood client', 'Works with Driftwood DB', 'Driftwood-certified'],
        answer: 1,
        why: 'It names the product to say what yours connects to, and claims no relationship with its owner.',
      },
      {
        q: 'Does the MIT license of a project grant its trademark?',
        options: [
          'Yes, everything is MIT',
          'No, licenses do not grant trademarks',
          'Only the logo',
        ],
        answer: 1,
        why: 'Copyright licenses cover the work. Trademarks are a separate right, and Apache-2.0 even says so outright.',
      },
    ],
  },
  '07': {
    note: 'Nobody chose colorwheel. It came along with prettyout. Read the whole tree, not just your own requirements, and let CI stop new licenses you have not approved.',
    quiz: [
      {
        q: "When do a dependency's license conditions apply to you?",
        options: [
          'Whenever it is listed in requirements.txt',
          'When you distribute it, for example in a bundle or image',
          'Never, dependencies are their own problem',
        ],
        answer: 1,
        why: 'Most licenses set conditions on distribution. A Docker image, desktop app or JavaScript bundle distributes everything inside it.',
      },
      {
        q: 'A package is under BUSL-1.1. What is it?',
        options: ['Permissive', 'Copyleft', 'Source-available, not open source'],
        answer: 2,
        why: 'BUSL limits production use until a change date. You can read the code, but you may not use it freely.',
      },
    ],
  },
  '08': {
    note: 'The GPL is about copies. The AGPL is also about users: change an AGPL program and let people use it online, and you must offer them the source of your version.',
    quiz: [
      {
        q: 'You run an unmodified AGPL database behind your web app. Must you publish your app?',
        options: [
          'Yes, AGPL spreads to everything',
          'No, you changed nothing',
          'Only the frontend',
        ],
        answer: 1,
        why: 'Section 13 applies to modified versions that users interact with. Using an unmodified AGPL server does not put your app under the AGPL.',
      },
      {
        q: 'Where should your AGPL source link point?',
        options: [
          'The upstream project',
          'The source of the exact version you run',
          'Your company homepage',
        ],
        answer: 1,
        why: 'Users are talking to your changed version, so the offer must lead to that source, kept in step with what is deployed.',
      },
    ],
  },
}

export function notesFor(pathname: string): Notes {
  const chapter = /^\/workshop\/(\d{2})-/.exec(pathname)?.[1]
  if (chapter && CHAPTERS[chapter]) return CHAPTERS[chapter]
  return pathname.startsWith('/workshop') ? WORKSHOP : HOME
}
