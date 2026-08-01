// ============================================================
// portfolioData.js — Centralized configuration for Ali Iftikhar's Portfolio
// All external links, personal info, and content in one place.
// Update this file to change any content across the entire site.
// ============================================================

export const personalInfo = {
  name: "Ali Iftikhar",
  firstName: "Ali",
  brandName: "Ali Iftikhar",
  title: "Digital Marketing & AI Automation Specialist",
  location: "Lahore, Pakistan",
  phone: "+92 327 4122476",
  emails: {
    primary: "aliiftikhar0601@gmail.com",
    secondary: "aliiftikhar0601@gmail.com",
  },
  summary:
    "Results-driven Digital Marketing professional with 4+ years of experience in Social Media Management (SMM), SEO campaigns, AI automations, Performance Marketing, and B2B Lead Generation. Proven track record of growing organic engagement by 25-500% MoM across international clients in UAE, Canada, USA, and Pakistan.",
  resumeUrl: "/Ali_Iftikhar_Resume.pdf",
};

export const socialLinks = {
  github: "https://github.com",
  linkedin: "https://linkedin.com/in/aliiftikhar",
  instagram: "https://instagram.com",
  website: "https://thealistyles.carrd.co",
};

export const heroContent = {
  greeting: "Hi, I'm Ali Iftikhar",
  titleHighlight: "Digital Marketing & AI Specialist",
  subtitle:
    "I scale brands, drive 500% MoM organic growth, execute SEO campaigns, and engineer AI-powered marketing automations.",
  ctaPrimary: { text: "View My Work", href: "#projects" },
  ctaSecondary: {
    text: "Contact Me",
    href: "mailto:aliiftikhar0601@gmail.com?subject=Hiring Inquiry – Portfolio&body=Hello Ali Iftikhar,%0D%0A%0D%0AI came across your portfolio and would like to discuss an opportunity with you.%0D%0A%0D%0ALooking forward to hearing from you.%0D%0ABest Regards,",
  },
  ctaResume: { text: "Download Resume", href: "/Ali_Iftikhar_Resume.pdf" },
};

export const aboutContent = {
  heading: "Hello!",
  bio: `Hi, my name is <span class="text-black text-xl font-black mx-1 tracking-wide uppercase">Ali Iftikhar</span>, a results-driven digital marketer and AI automation specialist based in Lahore, Pakistan. With over 4 years of hands-on experience, I help international brands scale their organic reach, generate high-converting B2B leads, and automate marketing workflows.`,
  techStack: ["Social Media", "SEO & Analytics", "AI Automations"],
};

export const skillsContent = {
  badge: "My Process",
  heading: "Here's how I turn brand strategies into measurable ROI",
  description:
    "I follow a structured, data-backed, and creative workflow to transform campaigns into high-converting revenue channels.",
  cards: [
    {
      number: "01",
      title: "Research",
      text: "In-depth audience profiling, competitor analysis, and market keyword research to lay a rock-solid foundation for the campaign.",
    },
    {
      number: "02",
      title: "Strategy",
      text: "Designing multi-platform content calendars, funnel architecture, brand positioning, and AI-driven workflow automations.",
    },
    {
      number: "03",
      title: "Execute",
      text: "Launching targeted paid ad campaigns, cold outreach SDR pipelines, and crafting high-impact visual content.",
    },
    {
      number: "04",
      title: "Optimize",
      text: "Continuous KPI tracking, performance analytics, A/B testing, and MoM engagement growth scaling.",
    },
  ],
  endText: "Ready to scale!",
};

// Technical & Digital Marketing Skills Data
export const technicalSkills = {
  categories: [
    {
      title: "Social Media & Brand Growth",
      skills: [
        { name: "SMM Strategy", level: 95 },
        { name: "Organic Growth", level: 94 },
        { name: "Content Creation", level: 92 },
        { name: "Brand Positioning", level: 90 }
      ]
    },
    {
      title: "SEO & Growth Analytics",
      skills: [
        { name: "SEO Campaigns", level: 90 },
        { name: "Off-page SEO", level: 88 },
        { name: "Keyword Strategy", level: 92 },
        { name: "KPI Analytics", level: 85 }
      ]
    },
    {
      title: "Generative AI & Automation",
      skills: [
        { name: "AI Prompting", level: 94 },
        { name: "n8n Automations", level: 88 },
        { name: "Workflow Automation", level: 90 },
        { name: "AI Creative Testing", level: 92 }
      ]
    },
    {
      title: "Lead Gen & SDR Outreach",
      skills: [
        { name: "SDR Cold Calling", level: 92 },
        { name: "Apollo.io & Scraping", level: 88 },
        { name: "Lead Qualification", level: 90 },
        { name: "B2B Outreach", level: 94 }
      ]
    },
    {
      title: "Tools & Platforms",
      skills: [
        { name: "Meta Ads Manager", level: 90 },
        { name: "Google Ads & Analytics", level: 88 },
        { name: "Canva Pro & Visual Design", level: 95 },
        { name: "LinkedIn Sales & Upwork", level: 92 }
      ]
    },
    {
      title: "Core Competencies",
      skills: [
        { name: "Market Research", level: 92 },
        { name: "Business Development", level: 88 },
        { name: "Team Mentoring", level: 90 },
        { name: "Campaign ROI Optimization", level: 94 }
      ]
    }
  ]
};

// Content Creation Data
export const contentCreation = {
  badge: "Visual Creatives & Campaigns",
  heading: "Creative Campaign Direction & Visual Assets",
  description: "Beyond strategy, I craft visual stories with premium ad graphics, packaging mockups, and social carousels.",
  categories: [
    {
      title: "Paid Ad Creatives",
      description: "Meta and Google ad graphics engineered for high click-through rates, brand recall, and customer acquisition.",
      stats: "100+ Ads Launched",
      icon: "🎯"
    },
    {
      title: "Social Post Campaigns",
      description: "Eye-catching carousel and single-post designs maintaining brand voice across global clients in UAE, USA, and Canada.",
      stats: "500+ Graphics Designed",
      icon: "🎨"
    },
    {
      title: "Packaging & Product Mockups",
      description: "Rigid box, beard oil, and perfume packaging visuals created for BlackBird Packaging.",
      stats: "Client Projects",
      icon: "📦"
    },
    {
      title: "Organic Reach & Reels",
      description: "Short-form video edits and engaging reels driving up to 500% MoM organic growth on LinkedIn and Instagram.",
      stats: "180k+ Impressions",
      icon: "📈"
    }
  ]
};

// Leadership & Work Activities Data
export const leadershipList = [
  {
    title: "SEO Campaign SDR Lead – Snexus Pvt Limited",
    description: "Executing targeted cold-calling campaigns to generate qualified leads, market research, and script alignment with live SEO campaigns.",
    role: "SDR Campaign Lead",
    badge: "Lead Gen"
  },
  {
    title: "Marketing Manager – Black Bird Digital",
    description: "Directing cross-channel social and paid ad campaigns across UAE, Canada, USA & Pakistan. Mentored teams and automated reporting.",
    role: "Marketing Manager",
    badge: "Leadership"
  },
  {
    title: "Social Media Lead – Adspectra",
    description: "Led social media strategy for Adspectra, driving 500% MoM LinkedIn engagement growth through targeted content strategies.",
    role: "SMM Lead",
    badge: "Organic Growth"
  },
  {
    title: "B2B Talent Acquisition & Upwork Bidding",
    description: "Managed Upwork bidding for recruitment projects generating $400+ USD in revenue; supported talent acquisition and interview coordination.",
    role: "Business Dev Lead",
    badge: "Co-Curricular"
  }
];

// Internships & Work Experience Data
export const internshipsList = [
  {
    organization: "Snexus Pvt Limited, Lahore",
    role: "SEO Campaign SDR",
    duration: "December 2025 - Present",
    skills: ["Cold Calling Campaigns", "SEO Service Promotion", "Market Research", "KPI Tracking"],
    tech: ["SEO Analytics", "Cold Outreach", "CRM", "Pipeline Tracking"]
  },
  {
    organization: "Black Bird Digital (Remote Agency)",
    role: "Marketing Manager & Specialist",
    duration: "December 2024 - Present",
    skills: ["Cross-Channel Campaigns", "AI Automations", "Team Mentoring", "Brand Strategy"],
    tech: ["Meta Ads", "n8n", "AI Prompting", "Canva Pro"]
  },
  {
    organization: "OryxCom / Comhub / Adspectra",
    role: "Social Media Manager",
    duration: "Sept 2023 - Dec 2024",
    skills: ["Content Strategy", "LinkedIn Organic Growth", "Upwork Bidding", "Consumer Insights"],
    tech: ["LinkedIn Ads", "Social Analytics", "Upwork", "Canva"]
  },
  {
    organization: "MuffleCo & Oryx Custom Boxes",
    role: "Social Media & Growth Lead",
    duration: "2024 (Onsite / Project)",
    skills: ["Lead Data Scraping", "CEO Branding", "Behance Setup", "Organic Growth"],
    tech: ["Apollo.io", "Google Maps Scraper", "Behance", "Email Marketing"]
  }
];

// Soft Skills Data
export const softSkillsList = [
  { name: "Leadership", icon: "👑", desc: "Guiding marketing teams, defining scope of work, and mentoring talent to achieve campaign goals." },
  { name: "Public Speaking & SDR", icon: "🎤", desc: "High-volume cold calling, objection handling, and articulate client communication." },
  { name: "Strategic Thinking", icon: "🧠", desc: "Aligning creative content with measurable business KPIs, pipeline growth, and ROI." },
  { name: "Adaptability", icon: "🌟", desc: "Rapidly mastering AI tools like n8n, Generative AI prompting, and new marketing platforms." },
  { name: "Problem Solving", icon: "🧩", desc: "Transforming low-converting funnels into high-yield lead generation pipelines." },
  { name: "Negotiation & SDR", icon: "🤝", desc: "Qualifying shippers/carriers, negotiating freight rates, and closing service deals." },
  { name: "Creativity", icon: "🎨", desc: "Designing aesthetic social assets, packaging mockups, and engaging ad visuals." },
  { name: "Time Management", icon: "⏰", desc: "Balancing multi-client agency portfolios across UAE, Canada, USA, and Pakistan." }
];

export const projects = [
  {
    id: "blackbird-packaging",
    number: "01",
    badge: "🚀 Flagship Campaign",
    title: "BlackBird Packaging & Brand Media Campaign",
    description:
      "Comprehensive digital marketing and visual content strategy for BlackBird Packaging. Designed high-impact packaging mockups (rigid boxes, perfume packaging, beard oils), managed ad testing, and executed cross-channel growth campaigns driving 30%+ MoM reach increase.",
    techTags: [
      "Social Media Strategy",
      "Canva Pro",
      "Packaging Mockups",
      "Meta Ads",
      "AI Content",
      "Brand Positioning"
    ],
    links: {
      github: null,
      demo: "https://thealistyles.carrd.co",
    },
    isFlagship: true,
  },
  {
    id: "adspectra-growth",
    number: "02",
    badge: null,
    title: "Adspectra Organic Reach & 500% MoM Growth",
    description:
      "Engineered organic social media content and brand positioning for Adspectra, generating 500% MoM growth in LinkedIn engagement and scaling organic post reach past 180k+ total impressions.",
    techTags: ["LinkedIn Organic", "Content Strategy", "SMM", "Analytics", "Brand Voice"],
    links: {
      github: null,
      frontendDemo: "https://thealistyles.carrd.co",
      backendApi: null,
    },
    isFlagship: false,
  },
  {
    id: "b2b-lead-gen",
    number: "03",
    badge: null,
    title: "B2B Lead Generation & Scraping Automation",
    description:
      "Architected end-to-end B2B lead generation workflows using Apollo.io, Google Maps scrapers, and n8n automations. Extracted over 10,000+ targeted business leads for UAE home cleaning services and US freight brokerage.",
    techTags: ["Lead Gen", "Apollo.io", "Data Scraping", "n8n Automations", "Cold SDR"],
    links: {
      github: null,
      demo: "https://thealistyles.carrd.co",
    },
    isFlagship: false,
  },
];

export const certificates = {
  featured: [
    {
      name: "Foundations of Digital Marketing & E-commerce",
      issuer: "Google (Coursera)",
      icon: "🎯",
    },
    {
      name: "Social Media & Social Content Strategy",
      issuer: "Digital Marketing Institute",
      icon: "📱",
    },
    {
      name: "Mega Digital Marketing Course A-Z (32 Courses)",
      issuer: "Udemy",
      icon: "🚀",
    },
    {
      name: "Generative AI for Digital Marketers",
      issuer: "LinkedIn Learning",
      icon: "🧠",
    },
    {
      name: "Email Marketing & Off-Page SEO Internship",
      issuer: "Industry Certified",
      icon: "✉️",
    },
    {
      name: "Organic Marketing & Traffic Growth",
      issuer: "Professional Certification",
      icon: "📈",
    },
  ],
  viewAllUrl: "/Ali_Iftikhar_Portfolio_Deck.pdf",
};

export const education = {
  degree: "Intermediate & Matriculation in Computer Science",
  institution: "American Lycetuff School & Digital Learning",
  cgpa: "Computer Science Major",
  graduation: "2020 - 2022",
  twelfth: "Intermediate CS (Self-directed Digital Focus)",
  tenth: "Matriculation Computer Science",
};

export const footerContent = {
  taglines: [
    "Digital Marketing & SMM Specialist",
    "SEO Campaigns · Paid Ads · AI Automations",
    "B2B Lead Generation & SDR Outreach",
  ],
  credential: "4+ Years Experience · 500% MoM Organic Growth",
  copyright: `© ${new Date().getFullYear()} Ali Iftikhar | Digital Marketing Portfolio`,
};

// EmailJS Configuration
export const emailjsConfig = {
  serviceId: import.meta.env.VITE_EMAILJS_SERVICE_ID || "YOUR_EMAILJS_SERVICE_ID",
  templateId: import.meta.env.VITE_EMAILJS_TEMPLATE_ID || "YOUR_EMAILJS_TEMPLATE_ID",
  publicKey: import.meta.env.VITE_EMAILJS_PUBLIC_KEY || "YOUR_EMAILJS_PUBLIC_KEY",
};
