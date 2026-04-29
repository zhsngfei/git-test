# Weizhi Product Design

## Purpose

Weizhi is a mobile-first travel-before-arrival culture app. It helps users enter a city before they physically arrive by giving them a curated city notebook of books, films, and cultural place touchpoints.

This first version is a real launchable product, not a static prototype or internal demo.

The product promise is:

> Before arriving in a city, users can understand part of its mood, rhythm, and stories through a small set of real works and places.

## Product Positioning

Weizhi is not a conventional travel guide, route planner, content feed, or generic AI chat tool.

It is a city culture preparation app:

- Users search for a city they will visit or want to understand.
- Users optionally choose content types and theme-tone tags.
- The app returns a city notebook made from real source-backed content.
- AI helps rank, group, and explain the recommendations.
- AI does not invent works, places, or facts.

## First-Version Strategy

The first version uses a curated-city strategy while preserving the product structure needed for future arbitrary-city support.

The app formally supports a selected East Asian city pool:

- Tokyo
- Kyoto
- Taipei
- Hong Kong
- Shanghai
- Beijing
- Kamakura
- Nara
- Seoul
- Hangzhou

Cities may have different content depth:

- Core cities have deeper coverage, richer work-place relationships, and more polished AI-reviewed recommendation groups.
- Expansion cities have lighter coverage, but must still have enough real content to avoid empty or generic recommendations.

Users can search for unsupported cities, but unsupported results show a refined "content is still being prepared" state instead of low-quality generated content.

## Platform

The first version is a mobile-first Web App / PWA.

It must be deployable and usable by real users:

- Real database-backed content.
- Real login.
- Persistent user collections.
- Real content import workflow.
- AI-supported recommendation flow with fallback states.
- Production-minded loading, empty, and error states.

The specific technical stack will be decided later. The product design assumes the system can support authentication, database storage, AI calls, caching, CSV/Excel content import, and deployment.

## Content Scope

First-version content types:

- Books
- Films

Reserved content type:

- Series

The data model should reserve the `series` type, but first-version UI does not need to promote series as a primary filter.

## Theme-Tone Tags

The product uses "theme-tone tags" instead of generic mood labels.

Theme-tone tags represent the way a user wants to enter a city before travel. They combine emotional tone and cultural angle.

Example tags:

- Quiet
- Nostalgic
- Solitary
- Youthful
- Suspenseful
- Humanistic
- Classic
- City wandering
- Filmic
- Literary

These tags are used for:

- Homepage lightweight discovery.
- Search preference input.
- City result filtering.
- AI ranking and grouping.
- Recommendation group titles.

Example city result groups:

- Quietly entering Kyoto
- Tokyo's solitude and night
- Taipei's youth and rain
- Hong Kong streets in film
- Works for the night before departure

Users may search without selecting tags. The default result is the city's representative recommendation set.

## Core User Flow

1. The user opens the homepage and sees brand, city search, lightweight theme-tone tags, and a featured city or theme visual.
2. The user enters a city or opens a featured city/theme.
3. If the city is supported, the app opens the city result page.
4. If the city is unsupported or underfilled, the app shows a refined preparation state.
5. The user browses book and film recommendations grouped by theme-tone.
6. The user opens a work detail page to understand why the work is worth reading or watching before travel.
7. The user opens related place touchpoints from the work detail page.
8. The user can collect works or places.
9. If the user is not logged in, collecting opens an email magic-link login prompt.
10. After login succeeds, the original collection action completes.
11. The user opens the collection page to view a city-organized pre-departure notebook.

## Page Structure

### Homepage

The homepage balances action and atmosphere.

Above the fold:

- Brand name: Weizhi.
- Short brand line, such as "Enter a city before arriving."
- City search input.
- Lightweight theme-tone tags.
- One featured city or featured theme visual.

Below the fold:

- Selected East Asian city entries.
- Theme cards, such as "The night before departure", "Before traveling alone", and "Streets in film".
- A small set of popular works or place touchpoints.

The homepage must not feel like a plain search page or a noisy content feed.

### City Result Page

The city result page is the core experience. It should feel like a city notebook rather than a search result list.

It contains:

- City title.
- Short city-tone sentence.
- Current filters and theme-tone tags.
- Content type filter: All, Books, Films.
- Theme-tone recommendation groups.
- Work cards with a mixed card rhythm.

Each theme group uses:

- One prominent work card for the lead recommendation.
- Smaller lightweight cards for secondary works.

The prominent card should include image, title, type, short recommendation reason, city relation, and collect action.

The lightweight card should include image, title, type, short reason, and collect action.

### Work Detail Page

The work detail page balances persuasion and city connection.

It contains:

- Large visual.
- Work title.
- Type.
- Author, director, or creator fields where applicable.
- Short synopsis.
- Recommendation reason.
- Suggested reading or viewing moment.
- Explanation of how the work connects to the city.
- Related place touchpoints.
- Collect work action.
- Similar recommendations.

Card copy is concise and clear. Detail copy may be more literary, but must stay grounded and specific.

### Place Detail Page

The place detail page is a cultural touchpoint page, not a travel guide page.

It contains:

- Place image.
- Place name.
- City.
- Short introduction.
- Meaning in the related work.
- Why it is worth noticing after arrival.
- Related work entry.
- Collect place action.

The first version does not show map, route, opening hours, tickets, nearby food, or itinerary planning.

The data model should still reserve address, latitude, longitude, and map query fields for future map support.

### Collection Page

The collection page is a pre-departure notebook.

It is organized by city instead of by raw collection time.

Each city group shows:

- Number of collected works.
- Number of collected places.
- Recent collected items.
- Entry into city collection detail.

Inside a city collection detail, the page has two tabs:

- Works
- Places

The first version does not include want-to-read, want-to-watch, read, watched, visited, check-in, or progress states.

### Reserved Pages

The first version reserves but does not fully build:

- My / settings center.
- Content management backend.
- Series browsing.
- Map entry.

## User System

The first version requires login for collection.

Login method:

- Email magic link or email verification code.
- No password login.
- No phone login.
- No third-party login in the first version.

Browsing rules:

- Users can browse homepage, city result pages, work detail pages, and place detail pages without login.
- Users must log in to collect works or places.
- When an unauthenticated user clicks collect, a lightweight login modal appears.
- After successful login, the original collect action completes automatically.
- The collection page shows a gentle login prompt when opened by unauthenticated users.

Login copy should be calm and contextual, such as "Save this pre-departure notebook."

## Collection Model

The first version has one collection behavior.

Collectable entities:

- Work
- Place

The UI does not split collection into want-to-read, want-to-watch, or want-to-go.

Product meaning:

- Collecting a work means the user wants to keep it for reading or watching before departure.
- Collecting a place means the user wants to keep the cultural touchpoint for possible attention after arrival.

## Content Operations

The first version uses CSV/Excel as the content maintenance interface.

Content pipeline:

```text
Online research / manual source search
-> Manual selection and verification
-> CSV / Excel content library
-> Import into production database
-> AI ranking, grouping, and explanation
-> Frontend display
```

The app should not read CSV/Excel directly at runtime. The frontend reads from the application database.

Required content entities:

- City
- Work
- Place
- Work-city relationship
- Work-place relationship
- Image metadata
- Source link
- Source note
- Review status

The frontend does not display source links by default, but backend content must remain source-traceable.

## AI Recommendation Rules

AI is responsible for:

- Ranking candidate works based on city, content type, and theme-tone tags.
- Grouping recommendations into theme-tone sections.
- Writing short card reasons.
- Writing more complete detail-page reasons.
- Writing short city-tone sentences.

AI is not allowed to:

- Invent works.
- Invent places.
- Invent relationships between works and cities.
- Invent relationships between works and places.
- Output facts outside the database.

AI receives verified database content as its factual context.

## AI Generation Mode

The first version uses a hybrid generation model.

Pre-generated path:

- Common city and theme-tone combinations are generated in advance.
- Pre-generated output is cached.
- Pre-generated output is manually reviewed before publication.

Real-time path:

- Uncommon combinations may be generated in real time.
- Real-time generation can only use verified database facts.
- Real-time generation is cached after creation.
- Real-time generation can later enter an internal review queue.

Fallback path:

- If AI generation fails, the app falls back to the city's default recommendation set.
- If a city has too little content, the app shows a preparation state instead of forcing weak recommendations.

## Feedback

The first version does not include a full feedback system.

It provides an email feedback entry for:

- Incorrect content.
- Image issues.
- City recommendations.
- General product feedback.

## Visual Direction

The visual direction is modern city notebook.

It should feel:

- Modern.
- Clean.
- Light.
- Quiet.
- Human.
- Image-aware.
- Editorial, but still product-like.

It should not feel:

- Like an old newspaper.
- Like an old book.
- Yellowed, antique, or heavily retro.
- Like a conventional travel guide app.
- Like a cold content management dashboard.
- Like a generic AI chat interface.
- Like a noisy social content feed.

Visual principles:

- Light modern palette.
- Clean whitespace.
- Strong but stable image areas.
- Book covers, film stills, and city photos create hierarchy.
- Short text blocks.
- Lightweight tags.
- Clear collection affordance.
- Subtle motion only for state changes.
- No decorative retro texture, yellowed paper, antique serif imitation, or old-newspaper layout.

Accessibility and usability principles:

- Mobile-first layout.
- Body text no smaller than 16px.
- Touch targets sized for mobile use.
- Sufficient text contrast.
- Meaningful image alt text.
- Stable image aspect ratios to avoid layout shift.
- Clear loading, empty, error, and unsupported-city states.
- Reduced-motion-friendly interaction design.

## First-Version In Scope

- Mobile-first Web App / PWA.
- Homepage search and theme-tone discovery.
- Ten selected East Asian cities.
- Book and film recommendations.
- Reserved series data type.
- City result page with theme-tone groups.
- Work detail page.
- Place detail page.
- Email magic-link or email-code login.
- Login-required collection.
- Work and place collection.
- City-organized collection page.
- CSV/Excel content import into database.
- AI ranking, grouping, and explanation based on verified content.
- Pre-generated reviewed recommendations for common combinations.
- Real-time constrained AI recommendations for uncommon combinations.
- Email feedback entry.
- Loading, error, empty, unsupported-city, and underfilled-city states.

## First-Version Out of Scope

- Flights.
- Hotels.
- Route planning.
- Restaurants.
- Map entry.
- Opening hours.
- Tickets.
- Nearby recommendations.
- Check-ins.
- Visited status.
- Want-to-read or want-to-watch states.
- Reading or viewing progress.
- Full My / settings center.
- Content management backend.
- User comments.
- Community posts.
- User-generated public content.
- Real-time arbitrary-city online research.
- Frontend source display.
- Phone login.
- Password login.
- Third-party login.
- Native iOS or Android app.

## Acceptance Criteria

Product experience:

- A new user can search a supported city, view recommendations, open a work detail page, and open a related place touchpoint within one minute.
- Users can browse core content without logging in.
- Users understand why login is needed when they collect an item.
- After login, the original collection action completes.
- The collection page organizes saved works and places by city.
- Unsupported or underfilled cities never show low-quality forced recommendations.
- AI failure does not block browsing.

Content quality:

- Each formally supported city has displayable works.
- Core cities have deeper coverage than expansion cities.
- Every displayed work has a clear city relationship.
- Every displayed place has a clear work relationship or city touchpoint meaning.
- Every frontend fact can be traced to backend source fields.
- AI output contains no database-external facts.

Visual quality:

- The app reads as a modern city notebook, not old paper, old books, or old newspaper.
- The homepage balances search and atmosphere.
- The city result page has clear theme groups and card rhythm.
- Work and place images reserve layout space before loading.
- Mobile touch targets are comfortable.
- Text is readable and not dependent on low-contrast gray.
- Empty states remain refined and on-brand.

Operational quality:

- Content can be maintained in CSV/Excel and imported into the database.
- Pre-generated AI content can be reviewed before publication.
- Real-time AI output can be cached.
- Feedback can be sent through an email entry.
