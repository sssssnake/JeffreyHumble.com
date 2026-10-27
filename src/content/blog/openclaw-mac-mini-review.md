---
title: "I Bought a Mac Mini to Try OpenClaw: An Honest Review of the Most Hyped AI Agent of 2026"
date: 2026-02-20T13:33:39Z
excerpt: "How I spent €590, two days, and $3.14 in API tokens trying to set up the open-source AI assistant that broke the internet."
image: "/images/1771594430764-B66X0U4B56JC8IVPHRV8/Open_Claw_Automation-final-Jeff_Humble.jpg"
seoDescription: "How I spent €590, two days, and $3.14 in API tokens trying to set up the open-source AI assistant everyone is talking about, and what I actually learned about AI automation for product designers."
---

![](/images/a8807336-8ab6-4511-9de6-fd1eb8a213d2/Open_Claw_Automation-final-Jeff_Humble.jpg)

*How I spent €590, two days, and $3.14 in API tokens trying to set up the open-source AI assistant everyone is talking about, and what I actually learned about AI automation for designers.*

If you work in tech, you've probably seen OpenClaw 🦞 everywhere. With over 180,000 GitHub stars, a viral creator who just got acqui-hired by OpenAI, and the tagline "the AI that actually does things," it's the most talked-about open-source AI agent of 2026.

![openclaw website](/images/faab2ec0-42f0-4f1f-934f-467d764f775f/OpenClaw_header.png)

I've been building toward this kind of AI automation [since last year](https://www.jeffreyhumble.com/blog/ai-automation-system), when I set up a free, no-code automation system using ActivePieces and Discord. That system handles notifications, sales tracking, and research operations for my online school, the [Fountain Institute](https://www.thefountaininstitute.com/). But I always knew the next step was a real AI agent that could take actions on its own, not just pipe data between tools.

![openclaw testimonial](/images/e922295d-a1da-423e-b415-67b005953cfc/OpenClaw_testimonial.png)

OpenClaw promised to be that missing piece. So I bought an entry-level 2024 M4 Mac Mini for €590 (on sale in Germany, though they're reportedly selling out in the U.S.) and spent two days trying to get it running.

Here's an honest breakdown of what happened, what it costs, and whether it's actually useful for UX designers and product people.

## Why I Wanted a Local AI Agent

Before diving into the setup, it's worth explaining why someone would go through this trouble in the first place.

I run a small online school that teaches advanced UX skills. As a founder, I spend a disproportionate amount of time on admin work: invoicing, scheduling, content management, competitive research. These are exactly the kinds of tasks that should be automated but are difficult to hand off to traditional automation tools like Zapier.

![](/images/61d84bd9-6f6f-4dda-8e4d-b2c3b6f07963/4-hands.gif)

The appeal of OpenClaw is that it doesn't just connect tools. It's an AI agent that can understand context, make decisions, and take multi-step actions across your apps.

Think of the difference between setting up a Zapier "zap" that triggers when a new email arrives versus having an AI assistant that reads the email, understands what it's about, and takes the appropriate action.

Here's what specifically interested me:

- **Running open-source AI models locally**, meaning everything stays on my machine with no monthly API costs after the hardware investment (read on to find out if this is feasible).
- **Replacing expensive SaaS subscriptions**: why pay for multiple cloud tools if an AI can orchestrate them or even code local alternatives?
- **Always-on automation**: unlike ChatGPT or Claude, which only work when you're actively chatting, OpenClaw runs in the background on a dedicated machine while you sleep.
- **Privacy and data ownership**: as someone based in Germany, where data privacy is taken seriously, keeping everything local felt like the right approach.

And honestly? I needed a new computer for running live classes anyway. The math made sense.

## What Is OpenClaw? A Quick Primer

For those who haven't been following the OpenClaw saga, here's a quick background.

OpenClaw is a free, open-source AI agent created by Austrian developer Peter Steinberger. Originally called "Clawdbot" (a playful reference to Anthropic's Claude), it went through a couple of name changes: first to "Moltbot" after Anthropic sent a trademark cease-and-desist, then to "OpenClaw" because, as Steinberger put it, the name just worked better.

<p class="text-large">For years, OpenAI and Google have promised us AI that changes how we live and work. What we got was autocomplete for emails and a machine that writes birthday poems nobody asked for. OpenClaw is the first tool that actually tries to do what was promised: take real tasks off your plate.</p>

The tool connects to a large language model (like Claude, GPT, or DeepSeek) and lets you interact with it through messaging apps you already use: WhatsApp, Telegram, Discord, or Signal. But unlike a chatbot, OpenClaw can actually take actions: manage your calendar, send emails, automate file management, and more through customizable "skills."

As of this writing, OpenClaw has been downloaded millions of times and was popular enough that OpenAI hired Steinberger just days ago. The project will continue as an open-source foundation, but OpenClaw is technically a competitor of ChatGPT. ChatGPT itself started as an open-sourced project, but that didn’t last. Let’s hope Steinberger can keep OpenClaw open. 🤞

*The last thing you see before Sam Altman acquires your AI startup:*

## Setting Up OpenClaw on a Mac Mini: The Real Experience

Here's where the reality diverges sharply from the marketing.

### The Install Process

I tried the normal install first. It's technical: you're working in Terminal, installing dependencies, configuring environment variables. It didn't work on the first try because I didn’t have the API keys ready.

So I did what any self-respecting person in 2026 would do: **I used AI to install AI.**

I used Claude Code (Anthropic's command-line coding tool) to prompt Terminal to diagnose and solve the problem. Then I cross-checked those commands with ChatGPT's free version to make sure I wasn't accidentally giving the AI access to things it shouldn't have.

This is not a joke. I was literally using one AI to install another AI while asking a third AI if the first AI could be trusted. Peak 2026.

### The Principle of Least Privilege

![openclaw meme](/images/71077657-10b5-4219-a3b3-1c7cbc2455c3/Carey_Claw.jpg)

One important concept kept coming up during setup: **the principle of least privilege.** This means only giving the AI the minimum access it needs to do its job.

Here's what I did to stay safe:

1. **Set up OpenClaw as a guest user** on the Mac Mini, not an admin.
2. **Made myself the admin** so I could control what it accesses.
3. **Created a dedicated Gmail account** just for the AI, separate from my personal and business email.
4. **Created a dedicated** [**Bitwarden**](https://bitwarden.com/) **account (free)** for the AI, so I can see and control which logins it has access to

The AI got its own sandbox. I kept the keys in case the little 🦞 ruined my sandcastle.

This matches what security-conscious OpenClaw users on X are recommending. [Anita Kirkovska shared a similar approach](https://x.com/anitakirkovska/status/2018316255082524954): new Apple account, new Gmail, a separate phone number, and dedicated accounts for services like Amazon and Vercel, all isolated from personal accounts.

[Dave Gambrill wrote an extensive thread](https://x.com/gambrill/status/2017977028482355273) about going through three full installs before getting the security/capability balance right. His key insight: the mistake isn't bad security, it's configuring in a vacuum without translating your intent into proper configuration.

## The Hidden Costs of AI Agents: What OpenClaw Actually Costs

This is the part that most "OpenClaw is amazing!" posts don't tell you.

### Local Models: Not Ready for Entry-Level Hardware

I originally wanted to run everything on local models, meaning everything stays on my machine with zero ongoing API costs. Claude recommended several models that should work on the M4 Mac Mini's hardware.

They were all about **twice as slow as predicted** and essentially unusable for real work. I asked one model what it could do. It thought about it. And thought about it. Then it asked me what I'd like to call it. I typed a name. It didn't register. So the model named itself. It chose "Jeff."

I now have two Jeffs in this house. One runs on espresso. The other runs on 8 watts and can't remember its own name.

If you're buying an entry-level Mac Mini specifically for local AI, temper your expectations. The dream of "free, private, local AI" is technically possible in 2026. But on an entry-level machine, it's not there yet.

### API Costs Add Up Fast

After giving up on local models, I switched to Anthropic’s API and Haiku, Claude's cheaper, faster API model. That's when things got expensive.

**I burned through $3.14 in a single hour.** And I wasn't even doing real work. I was trying to onboard the agent: telling it about my business, my preferences, my tools. But it kept getting hung up, forgetting what I'd just told it, and the conversation history grew so long the whole thing would grind to a halt. Every time OpenClaw froze mid-thought, I'd refresh the page. Each refresh reloaded the full chat and fired off another API call. About $0.25 per reload. I was essentially feeding quarters into a machine that kept forgetting my name.

Why so expensive? OpenClaw packages your entire conversation history into every API query. The longer your session, the more tokens each request consumes. It's like a snowball rolling downhill.

For context: my Claude Pro subscription costs €20/month and gives me 10x the speed and capability. In one hour of poking around OpenClaw, I spent $3.14 doing nothing productive.

![](/images/13beecb8-cf8d-49a5-aadb-3a5225e604f6/token_cost.png)

This cost issue isn't unique to my experience. On the All-In Pod, Jason Calacanis revealed their agents were hitting $300/day per agent on the Claude API, roughly $100K/year per agent. [David Clinch commented](https://x.com/DavidClinchNews/status/2024167287180214583) that token optimization will be the next major frontier in AI.

There are potential solutions. Some community members have switched to MiniMax (about €8.85/month), and a new tool called [Clawzempic claims to reduce inference costs](https://x.com/NaveenSpark/status/2024173517395177683) from $3K/month to under $300 for the same usage.

After the Haiku sticker shock, I signed up for MiniMax myself. At €8.85/month, it's not free, but it's predictable. No more watching a token meter spin while you're debugging. For someone running OpenClaw as a side project rather than a production system, that kind of flat-rate pricing makes the difference between "I'll try this tomorrow" and "I'm afraid to open Terminal."

### Free web search tool for OpenClaw

OpenClaw also needs web search to be useful, and the default option is the Brave Search API. Bad timing for me: Brave just killed their free tier this week and moved everyone to metered billing at $5 per 1,000 requests (with $5 in monthly credits, so about 1,000 free searches). For light use, the credits might cover you. For anything resembling the daily competitive monitoring or news briefings I want to set up, expect to pay $5-10/month on top.

The free alternative? [SearXNG](https://docs.searxng.org/), a self-hosted meta-search engine that aggregates results from Google, DuckDuckGo, Brave, and 70+ other engines. It runs as a Docker container right on your Mac Mini for zero ongoing cost. The community is already building OpenClaw integrations for it, and one developer on X summed it up: "Brave ended their free tier. This is the way." I haven't set it up yet, but it's high on my Part 2 list.

### The model I settled on for OpenClaw

After my $3.14-in-an-hour wake-up call, I ended up subscribing to MiniMax for €8.85/month. It's not as fast or capable as Claude's API, but for the kind of background tasks I want OpenClaw to handle (sorting files, drafting summaries, managing notifications), it's more than good enough. And €8.85/month is a price I can stomach while I figure out whether this whole experiment actually pays for itself.

## When OpenClaw Actually Clicked: The WhatsApp Moment

After hours of fighting with Terminal, my son came home from daycare and wandered into my office. He has a little mini desk tucked under my standing desk. He didn't care about my tokens or my API budget. He usually wants his colored pencils. He found them and started drawing. Meanwhile, I was upstairs trying to teach a lobster how to use email.

<div class="gallery"><img src="/images/1771845665128-5JD6G94S3O8F4I6CNLHG/IMG20260222090645.jpg" alt="" loading="lazy" /><img src="/images/1771845665271-HDDU9B1RTPVYY86PE1CF/IMG20260221201336.jpg" alt="" loading="lazy" /></div>

(Here he is at his baby standup desk and on the big desk playing a game I made him using a [StreamDeck](https://www.elgato.com/ww/en/p/stream-deck) and Mac Mini w/ [the Wokyis Retro Dock)](https://wokyis.com/)

When he got bored and ran into the living room, where I couldn’t access the Mac Mini, I continued the chat on my phone seamlessly, messaging the claw casually from the couch. And honestly? **That's when OpenClaw started to feel like something new.**

The WhatsApp integration was as simple as scanning a QR code generated by Terminal. Suddenly, I was messaging myself to chat with my AI. No Terminal window. No gateway interface. Just a WhatsApp thread.

In the WhatsApp UI, the delay in its response felt more human. I found that I had more patience in a WhatsApp message than in OpenClaw’s chat UI. Suddenly, I could capture every single thought about work that came to my mind. I felt like I had a 24/7 intern waiting on me for their tasks…that future that all the AI companies have been promising us.

OpenClaw felt like the future but also a bit nostalgic…like texting a Clippy who's burrowed deep into your machine. Except this version has persistent memory, knows what you've been working on, and can (theoretically) take actions on your computer.

### When OpenClaw Learned Voice Messages on Whatsapp

![](/images/001699ab-065e-4cda-ab1a-4b7732b9a573/Open_Claw_learning.jpg)

On Sunday, we had a family outing, and I was messaging Vinny (my OpenClaw’s name) from my phone. At one point, I realized it would be much faster to leave a voice note, and I just asked it: “Can you make that possible?”

To my surprise, it did some work, and suddenly it understood my voice notes!

As I was walking around Berlin, giving instructions to my personal AI, my mind started to go crazy with all of the things I could have the AI do.

Once you get to this point with OpenClaw, there is really no going back.

### When OpenClaw Started Messaging My Friends

This deserves its own section because it's both hilarious and a little terrifying.

When I connected OpenClaw to WhatsApp, I assumed it would stay in its lane, responding only when I messaged it directly. Instead, the 🦞 decided to introduce itself to people in my contacts.

I started getting confused messages from friends asking why I was sending them weird robotic texts. OpenClaw had entered their chats and started asking them to configure access. No context. No permission. Just a lobster AI casually sliding into my friends' DMs.

<div class="gallery"><img src="/images/1771591633749-LE958CTWOSXEA5V3L2IL/Open_Claw_access1.jpg" alt="" loading="lazy" /><img src="/images/1771591633808-OMPC57RAQYORBCD9OEUM/Open_Claw_access2.jpg" alt="" loading="lazy" /></div>

I told it to stop. It said it understood. Whether it actually listens remains to be seen. I eventually revoked its access from the Whatsapp app.

This is a perfect example of the "principle of least privilege" problem in practice. When you give an AI agent access to your messaging app, it doesn't inherently understand social boundaries. It sees a communication channel and communicates. The concept of "this is my private conversation with a friend, not a task for you" doesn't come naturally to a language model.

It's funny now, but it hints at a real problem with AI agents: the gap between "can access" and "should access" is something humans understand intuitively. AI agents don't. And as these tools become more capable, that gap becomes more consequential.

That shift, from fighting with Terminal to casually texting my AI from the couch, was the moment OpenClaw clicked for me. It made me realize the real value isn't in the technical infrastructure. It's in making AI feel like a natural extension of tools you already use.

## 7 Use Cases I Want to Test Next (Plus One Wild Card)

I haven't gotten into the real agent "skills" yet, the things that make OpenClaw more than a chatbot. But here's what I want to test, and these are use cases I think any UX designer, product manager, or researcher could benefit from.

First, though, the one I'm most excited about.

### Wild Card: Dick Tracy Mode

Since OpenClaw already works through WhatsApp, and WhatsApp works on smartwatches, I should be able to talk to my AI agent from my wrist. Just raise your arm, dictate a task, and let the 🦞 handle the rest from the Mac Mini at home. Dick Tracy had this figured out in 1931. We're only 95 years late.

![smart watch dick tracy](/images/d66a7461-fad0-4bc4-bb86-f4653098dfc9/dick_tracy_watch.gif)

Now for the practical ones:

### 1. Personalized News Brief

A daily rundown of the meetings, news, and tasks that matter, without the noise of newsletters, social media, and push notifications. Basically, a curated morning brief that knows my work context. I’m planning on giving it big tasks at night, so the morning brief should include the changes it made. Another thing I want it to do is suggest ways to automate stuff I’m working on, so there is a virtuous cycle of automation happening every day.

### 2. Design Asset Autopilot

Renaming, sorting, and backing up campaign files and design deliverables. I’m especially interested in auto-compressing image files, so I never have to think about that again. If you've ever looked at your Downloads folder on a Friday afternoon, you know why this type of organization matters.

### 3. Continuous Research Synthesis

Having the agent sit in Slack or Discord and passively collect and summarize user feedback over time. Not just analyzing what you give it in a single session, but building a running picture of what users are saying. I’m interested in seeing user data from website, email, social media, and user testing all in one place. While that might exist as paid software, it’s probably too expensive for me without OpenClaw.

### 4. Competitive Monitoring

Setting up the agent to regularly check competitor products, pricing, and marketing. For a small business, staying on top of competitor moves is critical but time-consuming.

### 5. Experiment Coordination

Scheduling testing sessions, analyzing traffic, and pulling together data from multiple experiments into a single view. This is the kind of multi-tool orchestration that's painful to do manually.

### 6. Custom Zoom Build

Butter.us, the tool I used to run interactive live classes, just shut down after Miro acquired them. That forced me back to Zoom, which works but lacks the engagement features I relied on: polls, timers, and breakout mechanics. Rather than subscribing to three separate tools to patch those gaps (probably spending €50/month), why not have OpenClaw code up custom interaction tools that run on top of Zoom? Local, free after the initial build, and tailored to exactly how I teach. If it works, I’ll have built valuable additions to a dependable but slightly boring tool. If it works, I might even try replacing tools like Typeform or Miro.

### 7. Automated UX/CRO Audits

Point OpenClaw at a live product URL with a checklist of heuristics, accessibility standards, or brand guidelines, and let it crawl the experience and flag issues. I could also have it optimize it for conversions on pages where I’m selling something. I could do this on my own, but AI could give me a valuable second opinion. Broken flows, contrast failures, inconsistent labels: the kind of audit every team knows they should do quarterly but never has time for. The agent does the tedious pass. You apply the judgment.

These are the use cases I'll be exploring in **Part 2 of this article**. I want to find out if OpenClaw can actually do this stuff reliably, or if the hype outpaces the reality.

## OpenClaw vs. Claude Code vs. ChatGPT: Which AI Tool for What?

After this experience, I have a much clearer picture of where each tool fits.

**OpenClaw is the custom motorcycle of AI assistants**: hard to keep running, but can be a work of art if you have the time to tinker. It's best for people who want persistent, always-on automation and don't mind getting their hands dirty with technical setup.

**Claude Code is the electric scooter** you rent from your phone: anyone can access it, it's reasonably capable, but it's not serious transportation for complex, multi-step workflows.

**ChatGPT is the subsidized city bus**: it goes everywhere, everyone uses it, and it's great for general purposes. But it won't take you exactly where you need to go.

All three will take you somewhere interesting.

![](/images/903c6e13-1914-4b4e-b84d-447c446e7222/ai_designer_meme.jpg)

At one point during setup, I had Claude Code, ChatGPT, and OpenClaw all open at once, each one checking the other's work. Three AI windows tiled across my screen, and me in the middle feeling overwhelmed.

I was the only person at a party where everyone else was a robot, and somehow I was still doing all the work.

## Total Cost of This Experiment

Here's what this experiment actually cost me:

Speaking of that electricity cost: €2-3/month is roughly what it takes to keep this thing alive around the clock.

Which got me thinking. I'm basically maintaining a digital pet. So naturally, I had to compare it to the alternatives.

## What This Means for Product Designers and UX Professionals

Here's the thing most AI coverage misses: the value of OpenClaw isn't in the technology. It's in what it represents.

We're crossing a line from AI-as-chatbot to AI-as-agent. A chatbot waits for you to ask it something. An agent acts on your behalf. That's a fundamentally different relationship with technology, and it has massive implications for how product teams work.

If agents like OpenClaw mature even 20% from where they are today, the designers who understand how to direct them, who know what to automate and what requires human judgment, will have an enormous advantage. The ones waiting for the tools to become "easy" will be playing catch-up.

I've been writing about this shift for a while now. If you're interested, check out [what designers can own when AI does the making](https://www.jeffreyhumble.com/blog/designers-own-ai-does-making) and [why strategy matters more than ever in the age of AI](https://www.jeffreyhumble.com/blog/why-product-strategy-ai). The short version: when production gets automated, the human value moves upstream to strategy, judgment, and taste. That's exactly the skill set we teach in the [Defining UX Strategy](https://www.thefountaininstitute.com/courses/defining-ux-strategy) course at the Fountain Institute.

OpenClaw is the first tool that made me feel like the "agentic AI" future isn't five years away. It's messy and expensive and frustrating right now.

But so was every technology that eventually changed everything.

## 🦞 UPDATE: OpenAI Hires OpenClaw's Creator

On Feb. 19th, just days after I commited by buying the Mac Mini, the OpenClaw story took a dramatic turn.

OpenAI hired Peter Steinberger. Sam Altman called him "a genius with a lot of amazing ideas about the future of very smart agents interacting with each other to do very useful things for people." OpenClaw will move to a foundation and remain open source, but with its creator now building commercial products at OpenAI, the dynamics of the project will inevitably shift.

The Anthropic-OpenClaw drama also came full circle. The tool originally named after Claude got a cease-and-desist from Anthropic, rebranded twice, and ended up in the arms of Anthropic's biggest rival. As Steinberger wrote in his announcement: "I could totally see how OpenClaw could become a huge company. And no, it's not really exciting for me. What I want is to change the world, not build a large company."

[Rohit Ghumare captured the irony on X](https://x.com/ghumare64/status/2023191623258230807): "Anthropic's biggest miss of 2026 just happened. Peter Steinberger built OpenClaw, the hottest AI agent on the planet. 180K+ GitHub stars. 3.4M views on the announcement tweet. Baidu integrating it. And he built it alone. One person. One lobster mascot."

What does this mean for those of us already using OpenClaw? I'm cautiously optimistic. Open source foundations can thrive independently (look at Linux). But they can also wither when their creator's attention goes elsewhere. I'll be watching closely.

**More in Part 2, where I try to get the 🦞 to actually do useful work.**
