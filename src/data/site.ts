// Site-wide settings: navigation, social links and footer links.
// Edit these and every page updates.

export const site = {
  name: "Jeff Humble",
  url: "https://www.jeffreyhumble.com",
  description:
    "Website of Jeffrey Humble・Jeff is an American designer, strategist, and educator living in Berlin",
  socialImage: "/images/111c9158-dff2-40d5-8024-cdfa0ea2a8ae/Utopian_Scholastic_Jeff_social_image.jpg",
};

export const nav = [
  { label: "About", href: "/about" },
  { label: "Consulting Services", href: "/services" },
  { label: "Free Resources", href: "/resources" },
  { label: "Blog", href: "/blog" },
];

export const social = [
  { label: "LinkedIn", href: "https://www.linkedin.com/in/jeff-humble/", icon: "linkedin" },
  { label: "YouTube", href: "https://www.youtube.com/channel/UCtVBDwEc-e60AqqvOXtzhGA", icon: "youtube" },
] as const;

export const headerCta = { label: "Jeff's Strategy Course", href: "https://bit.ly/4bgR5ml" };

export const footerColumns = [
  {
    title: "Learn about Jeff",
    links: [
      { label: "Home", href: "/" },
      { label: "About", href: "/about" },
      { label: "Portfolio", href: "/portfolio" },
      { label: "Resources", href: "/resources" },
      { label: "Blog", href: "/blog" },
    ],
  },
  {
    title: "Work with Jeff",
    links: [
      { label: "Consulting Services", href: "/services" },
      { label: "Speaking & Workshop Requests", href: "/speaking-requests" },
      { label: "Jeff’s Strategy Course", href: "https://www.thefountaininstitute.com/defining-ux-strategy" },
      { label: "Buy Jeff a Coffee", href: "https://buy.stripe.com/bIY5nvcJIeGIaXe14U" },
    ],
  },
];
