# RPTPN
> Replit Peer to Peer Network

## About
The RPTPN is a specification to allow for chatting, file sharing, code sharing, etc. Kinda like decentralized myspace ig??? idk its all in a cli (kinda) so its fun

## Spec
How stuff works

This was inspired by the dead Replit Blog Chat protocol me and Codemonkey51 started thinking up before the entire idea of a chat within the Replit Blog's logs died down. This is my best attempt at revitalizing it.

### Repl Name
To keep everything simplified, every repl running the protocol should be named rptpn. This simplifies storing information on other peers, which just makes evertything easier and much more straight forward.

### Discovery
Discovery is not only discouraged by me, but should be avoided in general. Having an entire network trying to ping `rptpn.[randomusername].repl.co` 24/7 would turn into a botnet faster than you think. This way, centralized directories (some of which are listed on [rptpn.com](https://www.rptpn.com/)) along with off-net communication are what will create links on the network.

### Establishing a Link
Repls running the service can either be unidirectional or bidirectional. A unidirectional repl could be something like a group chat or server, where only one repl needs to want to create the connection for it to be created. A service like this is not currently included in this example, but theres nothing stopping you from doing so and I might implement it later. A bidirection connection is where one repl wants to start a chat, and the other repl accepts it from a list of approved other users.

Establishing a link, whether it is unidirection or bidirectional, goes through the same process.

Endpoint|Request Type|Headers|Successful Return|Failed Return
-|-|-|-|-
`/api/link/new`|POST|`user` - The owner of the requesting repl. Can be pulled from the `$REPL_OWNER` environment variable.|`{'status': 'Link Established', 'additional_info': '[link_id]'}` - The [link_id] is a pseudo-random 8 digit number which allows for the initiating client to confirm the response they get back is actually from who they are sending it to.|`{'status': 'Failure', 'additional_info': 'Authentication Failed'}`
`/api/link/confirm`|WSS|`user` - The owner of the requesting repl. Can be pulled from the `$REPL_OWNER` environment variable. `link_id` - The link id provided from the previous request.|A secure websocket is established.|A failure happens, where the previous request is used to pass on the error, though a proper HTTP error code should be passed back to this request.

When Peer 1 wants to connect to Peer 2, they send a POST request to `/api/link/new` with their username as the `user` header. As a client cannot be inherently trusted, Peer 2 is who establishes the websocket connection with Peer 1 through `/api/link/confirm` and by passing along the link id, it can be fairly certainly assured that the link created is with its intended recipients. That way, if Peer 3 tries to pretend to be Peer 1 and establish a link with Peer 2, Peer 2 will simply try connecting to Peer 1, not Peer 3. Additionally, if Peer 3 tries establishing a link with Peer 2 at the same time Peer 1 is, only the connection with the correct link id will be established and the other will create an error. This way it is, in theory, impossible to pretend to be someone on the network. 

### Sending a Message
A message being sent on the network is pretty simple, though there are some guidelines to make sure cleanup occurs (where possible) and to allow for multimedia messages, of sorts. Do note, that the unofficial message limit is currently 500 characters, but since the sending client should handle adding a username and timestamp, splitting a longer message up is acceptable and possible.

Endpoint|Request Type|Body|Successful Return|Failed Return
-|-|-|-|-
(On an already established websocket)|N/A|`{'type': 'text', 'content': '[message]'}`|`{'status': 'Recieved', 'additional_info': 'Message Successful'}`|`{'status': 'Failure', 'additional_info': 'Some sort of message rendering error occured.'}`
(On an already established websocket)|N/A|`{'type': 'multimedia', 'content': '[link]'}`|`{'status': 'Recieved', 'additional_info': 'Message Successful'}`|`{'status': 'Failure', 'additional_info': 'Some sort of message rendering error occured.'}`
`/api/update`|POST|Anything can be sent for the body, as it causes the API to check for an update in the DB, as in any messages needing to be sent.If API spam is a concerned, a client creator can choose to use this body to send some sort of authentication token, though at this time it is not required in any way.|`Success`|`IDK how, but I somehow failed`

When it comes to an actual message, literally anything goes. A JSON object with it's type being `text` or `multimedia` and it's content either being an terminal-compatible ASCII string or the link to some sort of multimedia. It is literally that simple lol.

## Some Standards on the Client-Side
When it comes to a peer-to-peer network, technically anything goes, but some form of uniformity allows for the protocol to work. This protocol is quite simple, allowing for a lot to be built on top of it, along with clients not being restricted to the terminal. Here are a few things I reccomend you do with your client to keep it as speedy and user friendly as possible.

- Store the "friends" or users allowed to establish a connection in an environment variable, I reccomend that be `$RPTPN_FRIENDS`. This should be a JSON array, so if I'm allowing connections from `amasad`, `turbio`, and `roblockhead`, my `$RPTPN_FRIENDS` env variable would look like `['amasad', 'turbio', 'roblockhead']`. This means that switching from one client to another is as easy and quick as possible.
- Store the recent 100 messages from/to a user in the db as a JSON array where their key is `RPTPN_HISTORY_[USERNAME]`. Additionally, allow for the importing and exporting of these arrays to a JSON file to make it as easy as possible to move between clients. If you don't want to do it for your client to keep your clients locked in, they can simply do it themselves with the example in this file. Don't make it harder than it needs to.I should also mention that these shouldn't be plaintext strings of their message, but a JSON object to help differentiate who sent the message. They should follow this format:
```js
{
	'author': '[author_name]',
	'message_type': '[type of message]',
	'message_content': '[message content]'
}
```
- Store your websockets in a global object. This way both the "GUI" and API will both be able to make use of them.
- Keep you "GUI" and API on separate threads. In your CLI, you will have a "GUI" which should operate separately from the API. Keeping these separate allows for smoother operation and not having holdups for the user. Doing so is relatively easy, as they should both be able to access the same, aforementioned, global object.
- Try designing for a terminal with the width and height of 49x93 as this is the standard width and height of a Replit terminal on a 1080p screen. Also make sure whatever lib you use to determine the size of the terminal is accurate. In the case of Python, the function which comes with the `os` library is not accurate, but using the curses `curses.initscr().getmaxyx()` function will return the x and y size of the terminal. Curses also supports things like scrolling boxes, so it is perfect for pieces of text larger than a screen.
- Make it Asycnronous - I felt like this shouldn't need to be saying this, but you should probably make your client Asycnronous, especially if you're making your client a server.