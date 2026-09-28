# DealMind

## AI Deal Intelligence Agent with Persistent Memory

DealMind helps sales teams remember customer interactions and turn deal history into useful meeting intelligence.

## Problem

Sales conversations contain important details such as pricing objections, competitors, decision makers, technical concerns, and customer requests. DealMind keeps this context available through persistent AI memory.

## Core Features

- Capture customer interactions
- Store persistent memories using Hindsight
- Recall relevant deal information
- Generate personalized meeting preparation
- Show deal timeline and memory events

## Hindsight Usage

Retain: stores customer interactions as persistent memories.

Recall: retrieves relevant memories when a salesperson asks about a deal.

Reflect: uses accumulated context to generate a personalized meeting brief.

## Tech Stack

React, Vite, Python, FastAPI, Hindsight, JavaScript, HTML, and CSS.

## Example Deal

ACME Corp: pricing concerns, Salesforce evaluation, CTO technical concerns, flexible pricing request, and product demo request.

## Project Structure

DealMind/
  backend/
  frontend/
  README.md

## Running Locally

Backend: cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000

Frontend: cd frontend && npm run dev
