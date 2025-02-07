export interface Content {
  id: string
  content: string
  format_id: string
}

export interface Language {
  id: string
  code: string
  contents: Content[]
  formatted_contents: Record<string, string>
}

export interface Story {
  id: string
  title: string
  languages: Language[]
}