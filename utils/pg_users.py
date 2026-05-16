import streamlit as st
from utils.database import fetch, fetchone, run
from utils.styles import section_header, score_bar, category_banner, plotly_layout, render_footer
from utils.auth import require_admin, is_admin, hash_password


def show():
    require_admin()
    section_header("Manajemen User", "Role-Based Access Control", "👥")
    tab1, tab2 = st.tabs(["👤 Daftar User", "➕ Tambah User"])

    current_user = st.session_state.get("user", {})

    with tab1:
        rows = fetch(
            "SELECT id,username,full_name,role,email,is_active,created_at,last_login "
            "FROM users ORDER BY id"
        )

        for row in rows:
            rc = "#00d4ff" if row["role"] == "admin" else "#ffd700"
            ac = "#00ff88" if row["is_active"] else "#ff3366"
            label = ("🔑 " if row["role"]=="admin" else "👁 ") \
                    + (row["full_name"] or row["username"]) + "  @" + row["username"]

            with st.expander(label):
                c1, c2, c3 = st.columns([2,2,1])
                c1.markdown(f"**Username:** `{row['username']}`")
                c1.markdown(f"**Email:** {row['email'] or '-'}")
                ts = str(row.get('created_at') or '')[:10]
                c1.markdown(f"**Dibuat:** {ts}")
                c2.markdown(f"**Role:** <span style='color:{rc}'>{row['role'].upper()}</span>",
                            unsafe_allow_html=True)
                c2.markdown(
                    f"**Status:** <span style='color:{ac}'>"
                    f"{'AKTIF' if row['is_active'] else 'NONAKTIF'}</span>",
                    unsafe_allow_html=True)
                last = str(row.get("last_login") or "")[:16] or "Belum pernah"
                c2.markdown(f"**Login Terakhir:** {last}")

                if row["username"] != current_user.get("username"):
                    with c3:
                        lbl = "🔒 Nonaktifkan" if row["is_active"] else "✅ Aktifkan"
                        if st.button(lbl, key=f"tog_{row['id']}", use_container_width=True):
                            run("UPDATE users SET is_active=%s WHERE id=%s",
                                (0 if row["is_active"] else 1, row["id"]))
                            st.rerun()
                        if row["username"] != "admin":
                            if st.button("🗑️ Hapus", key=f"del_{row['id']}",
                                         use_container_width=True):
                                run("DELETE FROM users WHERE id=%s", (row["id"],))
                                st.rerun()

                st.markdown("---")
                with st.form(f"edit_{row['id']}"):
                    new_name  = st.text_input("Nama Lengkap",
                                              value=row["full_name"] or "",
                                              key=f"nm_{row['id']}")
                    new_email = st.text_input("Email",
                                              value=row["email"] or "",
                                              key=f"em_{row['id']}")
                    new_role  = st.selectbox("Role", ["admin","viewer"],
                                             index=0 if row["role"]=="admin" else 1,
                                             key=f"rl_{row['id']}")
                    new_pw    = st.text_input(
                        "Password Baru (kosongkan jika tidak direset)",
                        type="password", key=f"pw_{row['id']}")
                    if st.form_submit_button("💾 Simpan", use_container_width=True):
                        if new_pw:
                            run("UPDATE users SET password_hash=%s,role=%s,full_name=%s,email=%s WHERE id=%s",
                                (hash_password(new_pw), new_role, new_name, new_email, row["id"]))
                        else:
                            run("UPDATE users SET role=%s,full_name=%s,email=%s WHERE id=%s",
                                (new_role, new_name, new_email, row["id"]))
                        st.success("✅ User diupdate!")
                        st.rerun()

    with tab2:
        with st.form("add_user"):
            col1, col2 = st.columns(2)
            uname  = col1.text_input("Username*")
            upw    = col1.text_input("Password*", type="password")
            urole  = col1.selectbox("Role", ["viewer","admin"])
            ufull  = col2.text_input("Nama Lengkap")
            uemail = col2.text_input("Email")

            if st.form_submit_button("➕ Tambah User",
                                     use_container_width=True, type="primary"):
                if uname and upw:
                    try:
                        run("INSERT INTO users "
                            "(username,password_hash,full_name,role,email,is_active) "
                            "VALUES (%s,%s,%s,%s,%s,1)",
                            (uname, hash_password(upw), ufull, urole, uemail))
                        st.success(f"✅ User '{uname}' berhasil ditambahkan sebagai {urole}!")
                        st.rerun()
                    except Exception as e:
                        if "unique" in str(e).lower():
                            st.error(f"❌ Username '{uname}' sudah digunakan.")
                        else:
                            st.error(f"❌ Error: {e}")
                else:
                    st.error("❌ Username dan password wajib diisi.")
