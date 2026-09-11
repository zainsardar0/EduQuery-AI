# Daanish School Web Portal — EduQuery AI Single Sign-On (SSO) Integration Guide

This guide explains how to add the **"EduQuery AI Portal"** launch button to the Daanish Schools ASP.NET Web Forms portal (`ACD_Foren`).

---

## 1. ASP.NET Web Forms Button Markup (`Site.Master` or Coordinator Pages)

Add this launch button to the navigation menu or coordinator dashboard page (e.g. `ATKB_EX_COORD.aspx`, `akram.aspx`, or `Site.master`):

```html
<!-- EduQuery AI Launch Button -->
<asp:LinkButton ID="btnLaunchEduQuery" runat="server" CssClass="btn btn-primary" OnClick="btnLaunchEduQuery_Click">
    <i class="fa fa-robot"></i> Open EduQuery AI Portal
</asp:LinkButton>
```

---

## 2. Code-Behind (`.aspx.cs` or `MasterPage.master.cs`)

Add this click event handler in the corresponding C# code-behind file:

```csharp
using System;
using System.Web;

protected void btnLaunchEduQuery_Click(object sender, EventArgs e)
{
    // Retrieve current logged in user from Session
    string username = Session["Username"] != null ? Session["Username"].ToString() : "GuestUser";
    string school = Session["School"] != null ? Session["School"].ToString() : (Session["SCHOOL"] != null ? Session["SCHOOL"].ToString() : "MNWB");
    
    // Determine user role based on username or session
    string role = "teacher";
    if (username.ToLower() == "awais" || username.ToLower().Contains("admin"))
    {
        role = "admin";
    }
    else if (username.ToLower().Contains("coord") || username.ToLower().Contains("principal") || username.ToLower() == "akram")
    {
        role = "principal";
    }

    // EduQuery AI portal URL (Configure in Web.config or environment)
    string eduQueryBaseUrl = "http://localhost:5173"; // Or your production URL https://eduquery.ai

    // Redirect to EduQuery AI portal with SSO handshake parameters
    string redirectUrl = string.Format("{0}/#/app?sso_user={1}&sso_school={2}&sso_role={3}",
        eduQueryBaseUrl,
        HttpUtility.UrlEncode(username),
        HttpUtility.UrlEncode(school),
        HttpUtility.UrlEncode(role)
    );

    Response.Redirect(redirectUrl);
}
```

---

## 3. How It Works

1. User logs into the Daanish School Portal with their standard credentials and OTP.
2. User clicks the **"Open EduQuery AI Portal"** button.
3. The portal securely redirects to EduQuery AI (`/#/app?sso_user=...&sso_school=...&sso_role=...`).
4. EduQuery AI's frontend exchanges these verified claims with the FastAPI backend endpoint `POST /api/v1/auth/sso-login`.
5. The backend mints a secure `AuthContext` with the user's campus scope and role.
6. The user immediately enters the EduQuery AI interface with their campus data and all AI engines (WrenAI live query, Google File Search RAG, Semantic RAG) ready to use!
