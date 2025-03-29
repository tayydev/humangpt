// export interface Message {
//   id: string;
//   content: string;
//   role: 'user' | 'assistant';
//   timestamp: Date;
// }
//
// export interface Chat {
//   id: string;
//   title: string;
//   messages: Message[];
//   createdAt: Date;
// }

import type {Session} from "humangpt-client"
import type {Message} from "humangpt-client"
export type {Session, Message};
