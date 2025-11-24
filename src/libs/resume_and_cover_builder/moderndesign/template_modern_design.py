"""
Modern Design Templates for CV Generation
Professional layout with diagonal header and sidebar
"""

# Main Resume Template
MODERN_DESIGN_TEMPLATE = """
<div class="resume-page">
    <div class="header-zone">
        <div class="diagonal-gray"></div>
        <div class="top-blue-box">
            <div class="sidebar-content">
                <div class="contacts">
                    {{CONTACT_INFO}}
                </div>
            </div>
        </div>
        <div class="name-area">
            <div class="main-name">{{FULL_NAME}}</div>
            <div class="main-title">{{JOB_ROLE}}</div>
        </div>
    </div>

    <div class="left-side">
        <div class="left-content">
            <p class="intro-para">
                {{PERSONAL_SUMMARY}}
            </p>

            <div class="content-section">
                <h2 class="section-title">E X P E R I E N C E</h2>
                {{WORK_EXPERIENCE}}
            </div>

            <div class="content-section">
                <h2 class="section-title">E D U C A T I O N</h2>
                {{EDUCATION}}
            </div>

            {{PROJECTS_SECTION}}
            
            {{ACHIEVEMENTS_SECTION}}
            
            {{CERTIFICATIONS_SECTION}}
        </div>
    </div>

    <div class="right-sidebar">
        <div style="height: 1.5in;"></div>
        <div class="sidebar-content">
            <div class="sidebar-section">
                <h2 class="sidebar-header">S K I L L S</h2>
                {{SKILLS}}
            </div>

            {{INTERESTS_SECTION}}

            {{LANGUAGES_SECTION}}
        </div>
    </div>
</div>
"""

# Contact Info Template
CONTACT_ITEM_TEMPLATE = """
<div class="contact-row">
    <div class="icon">
        <svg viewBox="0 0 24 24"><path d="{{ICON_PATH}}"/></svg>
    </div>
    <div>{{CONTACT_TEXT}}</div>
</div>
"""

# Work Experience Item Template
WORK_EXPERIENCE_ITEM_TEMPLATE = """
<div class="work-item">
    <div class="dates">{{DATE_RANGE}}</div>
    <div class="details">
        <div class="position">{{POSITION_TITLE}}</div>
        <div class="description">
            {{JOB_DESCRIPTION}}
        </div>
        {{ACCOMPLISHMENTS}}
    </div>
</div>
"""

# Accomplishments Template
ACCOMPLISHMENTS_TEMPLATE = """
<div class="accomplishments">
    <div class="accomplishments-header">Major accomplishments:</div>
    <ul>
        {{ACCOMPLISHMENT_ITEMS}}
    </ul>
</div>
"""

# Education Item Template
EDUCATION_ITEM_TEMPLATE = """
<div class="work-item">
    <div class="dates">{{DATE_RANGE}}</div>
    <div class="details">
        <div class="position">{{DEGREE}} - {{SCHOOL_NAME}}</div>
        <div class="description">
            {{EDUCATION_DESCRIPTION}}
        </div>
    </div>
</div>
"""

# Skill Item Template
SKILL_ITEM_TEMPLATE = """
<div class="skill">
    <div class="skill-label">{{SKILL_NAME}}</div>
    <div class="dots">
        {{SKILL_DOTS}}
    </div>
</div>
"""

# Projects Section Template
PROJECTS_SECTION_TEMPLATE = """
<div class="content-section">
    <h2 class="section-title">P R O J E C T S</h2>
    {{PROJECT_ITEMS}}
</div>
"""

# Achievements Section Template
ACHIEVEMENTS_SECTION_TEMPLATE = """
<div class="content-section">
    <h2 class="section-title">A C H I E V E M E N T S</h2>
    {{ACHIEVEMENT_ITEMS}}
</div>
"""

# Interests Section Template
INTERESTS_SECTION_TEMPLATE = """
<div class="sidebar-section">
    <h2 class="sidebar-header">I N T E R E S T S</h2>
    {{INTEREST_ITEMS}}
</div>
"""

INTEREST_ITEM_TEMPLATE = """
<div class="hobby">
    <div class="hobby-title">{{INTEREST_NAME}}</div>
    <div class="hobby-text">
        {{INTEREST_DESCRIPTION}}
    </div>
</div>
"""

# Languages Section Template
LANGUAGES_SECTION_TEMPLATE = """
<div class="sidebar-section">
    <h2 class="sidebar-header">L A N G U A G E S</h2>
    {{LANGUAGE_ITEMS}}
</div>
"""

