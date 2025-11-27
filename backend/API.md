# API Documentation

## Base URL

```
http://localhost:3000
```

## Authentication

Currently, no authentication is required. This will be added in future versions.

## Rate Limiting

- **Generation endpoint**: 15 requests per 15 minutes
- **Other endpoints**: 100 requests per minute

## Response Format

All responses follow this structure:

### Success Response
```json
{
  "success": true,
  "data": { ... }
}
```

### Error Response
```json
{
  "success": false,
  "error": {
    "message": "Error description",
    "statusCode": 400
  }
}
```

## Endpoints

### 1. Generate Animation

Convert text description into animation instructions.

**Endpoint:** `POST /api/generate`

**Request Body:**
```json
{
  "text": "Animate the Pythagoras theorem with a growing square"
}
```

**Validation:**
- `text`: Required, 10-2000 characters

**Response:** `201 Created`
```json
{
  "success": true,
  "data": {
    "id": "507f1f77bcf86cd799439011",
    "inputText": "Animate the Pythagoras theorem...",
    "concept": {
      "topic": "Pythagoras Theorem",
      "objects": ["triangle", "square_a", "square_b", "square_c"],
      "actions": ["show_triangle", "grow_square_a", ...],
      "style": {
        "color": "cyan",
        "background": "dark"
      }
    },
    "scenes": [
      {
        "id": "scene1",
        "duration": 4,
        "objects": ["triangle"],
        "actions": [...]
      }
    ],
    "timeline": [
      {
        "time": 0,
        "target": "triangle",
        "action": "fade_in",
        "params": {
          "from": 0,
          "to": 1,
          "duration": 1
        }
      }
    ],
    "objects": {
      "triangle": {
        "type": "shape",
        "geometry": "triangle",
        "color": "cyan",
        "position": { "x": 0, "y": 0, "z": 0 },
        "scale": { "x": 1, "y": 1, "z": 1 }
      }
    },
    "audio": [
      {
        "time": 0,
        "clip": "intro.mp3"
      }
    ],
    "style": {
      "background": "#0f0f0f",
      "themeColor": "cyan"
    },
    "status": "completed",
    "createdAt": "2024-01-01T00:00:00.000Z",
    "updatedAt": "2024-01-01T00:00:00.000Z"
  }
}
```

**Example:**
```bash
curl -X POST http://localhost:3000/api/generate \
  -H "Content-Type: application/json" \
  -d '{"text": "Animate a bouncing ball with gravity"}'
```

---

### 2. Get Animation by ID

Retrieve a specific animation.

**Endpoint:** `GET /api/animation/:id`

**Parameters:**
- `id`: MongoDB ObjectId (24 hex characters)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": { ... }
}
```

**Errors:**
- `404`: Animation not found
- `400`: Invalid ID format

**Example:**
```bash
curl http://localhost:3000/api/animation/507f1f77bcf86cd799439011
```

---

### 3. List Animations

Get paginated list of all animations.

**Endpoint:** `GET /api/animations`

**Query Parameters:**
- `limit`: Number of results (1-100, default: 20)
- `skip`: Number to skip (default: 0)

**Response:** `200 OK`
```json
{
  "success": true,
  "data": [ ... ],
  "pagination": {
    "limit": 20,
    "skip": 0,
    "count": 15
  }
}
```

**Example:**
```bash
curl "http://localhost:3000/api/animations?limit=10&skip=0"
```

---

### 4. Delete Animation

Remove an animation from the database.

**Endpoint:** `DELETE /api/animation/:id`

**Parameters:**
- `id`: MongoDB ObjectId

**Response:** `200 OK`
```json
{
  "success": true,
  "message": "Animation deleted successfully"
}
```

**Errors:**
- `404`: Animation not found
- `400`: Invalid ID format

**Example:**
```bash
curl -X DELETE http://localhost:3000/api/animation/507f1f77bcf86cd799439011
```

---

### 5. Health Check

Check server and database status.

**Endpoint:** `GET /health`

**Response:** `200 OK`
```json
{
  "success": true,
  "status": "ok",
  "database": "connected",
  "timestamp": "2024-01-01T00:00:00.000Z"
}
```

**Example:**
```bash
curl http://localhost:3000/health
```

---

## Error Codes

| Code | Description |
|------|-------------|
| `400` | Bad Request - Invalid input |
| `404` | Not Found - Resource doesn't exist |
| `429` | Too Many Requests - Rate limit exceeded |
| `500` | Internal Server Error |

## Data Models

### Animation Object

The complete structure returned by the API:

```typescript
{
  id: string;                    // MongoDB ObjectId
  inputText: string;             // Original user input
  concept: {
    topic: string;
    objects: string[];
    actions: string[];
    style: {
      color: string;
      background: string;
    };
  };
  scenes: Array<{
    id: string;
    duration: number;
    objects: string[];
    actions: Array<{
      target: string;
      action: string;
      duration: number;
    }>;
  }>;
  timeline: Array<{
    time: number;
    target: string;
    action: string;
    params: {
      from?: number;
      to?: number;
      duration: number;
    };
  }>;
  objects: {
    [key: string]: {
      type: string;
      geometry: string;
      color: string;
      position?: { x: number; y: number; z: number };
      scale?: { x: number; y: number; z: number };
    };
  };
  audio: Array<{
    time: number;
    clip: string;
  }>;
  style: {
    background: string;
    themeColor: string;
  };
  status: 'pending' | 'processing' | 'completed' | 'failed';
  createdAt: Date;
  updatedAt: Date;
}
```

## Timeline Actions

Available animation actions:

- `fade_in`: Opacity 0 → 1
- `fade_out`: Opacity 1 → 0
- `scale_up`: Scale 0 → 1
- `scale_down`: Scale 1 → 0
- `move`: Position change
- `rotate`: Rotation change
- `pulse`: Pulsing effect
- `highlight`: Highlight object

## Geometry Types

Supported geometric shapes:

- `triangle`
- `square`
- `circle`
- `line`
- `rectangle`
- `pentagon`
- `hexagon`
