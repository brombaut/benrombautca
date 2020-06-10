export interface Project {
  id: number;
  name: string;
  description: string;
  techUsed: string[];
  url: string;
  sourceUrl: string;
  thumbnail: string;
  inProgress: boolean;
  acronym?: string;
}
