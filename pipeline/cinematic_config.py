"""
Cinematic Style Configuration for SIKHO Animation Generator

This module defines all visual style presets, color palettes, camera behaviors,
and animation parameters for producing professional-quality educational animations.
"""

# ══════════════════════════════════════════════════════════════════════════
# 🎨 COLOR PALETTES
# ══════════════════════════════════════════════════════════════════════════

PALETTES = {
    "blue-purple": {
        "primary": "#4F82FF",
        "accent": "#D788FF",
        "text": "#00FFFF",
        "background_dark": "#0A0A1A",
        "background_light": "#1A1A3A",
        "particle": "#4F82FF",
    },
    "red-orange": {
        "primary": "#FF4F4F",
        "accent": "#FF8C42",
        "text": "#FFD700",
        "background_dark": "#1A0A0A",
        "background_light": "#3A1A1A",
        "particle": "#FF6B6B",
    },
    "green-teal": {
        "primary": "#00D9A3",
        "accent": "#00B8D4",
        "text": "#A7FF00",
        "background_dark": "#0A1A14",
        "background_light": "#1A3A2A",
        "particle": "#00D9A3",
    },
    "monochrome": {
        "primary": "#FFFFFF",
        "accent": "#CCCCCC",
        "text": "#FFFFFF",
        "background_dark": "#0A0A0A",
        "background_light": "#1A1A1A",
        "particle": "#888888",
    },
}

# ══════════════════════════════════════════════════════════════════════════
# 🎬 THEME CONFIGURATIONS
# ══════════════════════════════════════════════════════════════════════════

THEMES = {
    "dark-neon": {
        "background_color": "#0A0A1A",
        "use_gradient": True,
        "gradient_colors": ["#0A0A1A", "#1A1A3A"],
        "particle_count": 40,
        "particle_opacity": 0.2,
        "glow_effects": True,
    },
    "light-minimal": {
        "background_color": "#F5F5F5",
        "use_gradient": False,
        "gradient_colors": ["#F5F5F5", "#FFFFFF"],
        "particle_count": 0,
        "particle_opacity": 0,
        "glow_effects": False,
    },
    "gradient-modern": {
        "background_color": "#1A1A2E",
        "use_gradient": True,
        "gradient_colors": ["#1A1A2E", "#16213E", "#0F3460"],
        "particle_count": 30,
        "particle_opacity": 0.15,
        "glow_effects": True,
    },
    "cyberpunk": {
        "background_color": "#000000",
        "use_gradient": True,
        "gradient_colors": ["#000000", "#0D0221", "#0F0A1E"],
        "particle_count": 50,
        "particle_opacity": 0.25,
        "glow_effects": True,
    },
}

# ══════════════════════════════════════════════════════════════════════════
# 📷 CAMERA CONFIGURATIONS
# ══════════════════════════════════════════════════════════════════════════

CAMERA_STYLES = {
    "static": {
        "movement": None,
        "description": "No camera movement - stable and focused",
    },
    "slow-zoom": {
        "movement": "scale",
        "scale_factor": 0.95,
        "run_time": 3.5,
        "rate_func": "smooth",
        "description": "Gentle zoom-in for emphasis",
    },
    "gentle-drift": {
        "movement": "shift",
        "shift_vector": {"UP": 0.1, "RIGHT": 0.05},
        "run_time": 4.0,
        "rate_func": "ease_in_out_sine",
        "description": "Subtle floating motion",
    },
    "dynamic": {
        "movement": "multiple",
        "movements": [
            {"type": "scale", "factor": 0.95, "time": 2.0},
            {"type": "shift", "vector": {"UP": 0.15}, "time": 2.5},
        ],
        "description": "Multiple camera movements throughout",
    },
}

# ══════════════════════════════════════════════════════════════════════════
# 🎭 MOTION CONFIGURATIONS
# ══════════════════════════════════════════════════════════════════════════

MOTION_STYLES = {
    "smooth": {
        "rate_func": "smooth",
        "default_run_time": 1.2,
        "wait_between_objects": 0.2,
        "wait_after_transitions": 1.0,
        "description": "Smooth, professional animations",
    },
    "energetic": {
        "rate_func": "rush_into",
        "default_run_time": 0.9,
        "wait_between_objects": 0.1,
        "wait_after_transitions": 0.6,
        "description": "Quick, dynamic movements",
    },
    "calm": {
        "rate_func": "ease_in_out_sine",
        "default_run_time": 1.6,
        "wait_between_objects": 0.3,
        "wait_after_transitions": 1.2,
        "description": "Slow, relaxing pace",
    },
    "professional": {
        "rate_func": "smooth",
        "default_run_time": 1.3,
        "wait_between_objects": 0.25,
        "wait_after_transitions": 1.0,
        "description": "Corporate, polished feel",
    },
}

# ══════════════════════════════════════════════════════════════════════════
# ✨ ANIMATION EFFECTS
# ══════════════════════════════════════════════════════════════════════════

ENTRANCE_ANIMATIONS = {
    "circle": "GrowFromCenter",
    "square": "GrowFromCenter",
    "rectangle": "GrowFromCenter",
    "text": "Write",
    "arrow": "GrowArrow",
    "line": "Create",
    "default": "FadeIn",
}

EMPHASIS_EFFECTS = {
    "flash": {"class": "Flash", "radius": 2.0, "run_time": 0.8},
    "indicate": {"class": "Indicate", "scale_factor": 1.2, "run_time": 0.6},
    "circumscribe": {"class": "Circumscribe", "fade_in": True, "run_time": 1.0},
    "wiggle": {"class": "Wiggle", "run_time": 0.5},
}

# ══════════════════════════════════════════════════════════════════════════
# 📏 SIZING & SPACING
# ══════════════════════════════════════════════════════════════════════════

FONT_SIZES = {
    "title": 54,
    "subtitle": 42,
    "body": 36,
    "caption": 28,
}

Z_INDEX_LAYERS = {
    "background": -1,
    "particles": -1,
    "base_objects": 0,
    "highlights": 1,
    "text": 2,
    "overlays": 3,
}

SPACING = {
    "title_position": {"direction": "UP", "buffer": 0.5},
    "subtitle_position": {"direction": "UP", "buffer": 2.5},
    "footer_position": {"direction": "DOWN", "buffer": 2.5},
}

# ══════════════════════════════════════════════════════════════════════════
# ⏱️ TIMING DEFAULTS
# ══════════════════════════════════════════════════════════════════════════

TIMING = {
    "intro_pause": 0.5,
    "min_object_animation": 1.2,
    "glow_effect": 0.7,
    "transition_wait": 1.0,
    "outro_pause": 2.0,
    "total_ideal_min": 8,
    "total_ideal_max": 15,
}

# ══════════════════════════════════════════════════════════════════════════
# 🎯 DEFAULT STYLE (FALLBACK)
# ══════════════════════════════════════════════════════════════════════════

DEFAULT_STYLE = {
    "theme": "dark-neon",
    "camera": "slow-zoom",
    "motion": "smooth",
    "palette": "blue-purple",
}


# ══════════════════════════════════════════════════════════════════════════
# 🛠️ HELPER FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════

def get_style_config(style_dict=None):
    """
    Get complete style configuration with defaults applied.
    
    Args:
        style_dict: Optional dict with theme, camera, motion, palette keys
        
    Returns:
        Complete style configuration dictionary
    """
    if not style_dict:
        style_dict = DEFAULT_STYLE
    
    config = {
        "theme": THEMES.get(style_dict.get("theme", "dark-neon"), THEMES["dark-neon"]),
        "camera": CAMERA_STYLES.get(style_dict.get("camera", "slow-zoom"), CAMERA_STYLES["slow-zoom"]),
        "motion": MOTION_STYLES.get(style_dict.get("motion", "smooth"), MOTION_STYLES["smooth"]),
        "palette": PALETTES.get(style_dict.get("palette", "blue-purple"), PALETTES["blue-purple"]),
    }
    
    return config


def get_entrance_animation(object_type):
    """Get the recommended entrance animation for an object type."""
    return ENTRANCE_ANIMATIONS.get(object_type.lower(), ENTRANCE_ANIMATIONS["default"])


def get_palette_color(palette_name, color_type):
    """Get a specific color from a palette."""
    palette = PALETTES.get(palette_name, PALETTES["blue-purple"])
    return palette.get(color_type, palette["primary"])
