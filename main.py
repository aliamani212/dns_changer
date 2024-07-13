import flet as ft
import subprocess


# global variables
primary = ft.TextField('',)
secondary = ft.TextField('')
system_primary = ft.TextField('',read_only=True)
system_secondary = ft.TextField('',read_only=True)

def main(page:ft.Page):
    
    # page setting
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_width=600
    page.window_height=400
    h = page.window_height=450
    w = page.window_width=600
    page.rtl = True
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.DNS),
        leading_width=40,
        title=ft.Text("dns changer"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
    )
    
    
    
    # functions
    def get_dns_servers():
        command = ["ipconfig", "/all"]
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("خطا در اجرای دستور ipconfig:")
            print(result.stderr)
            return
        
        dns_servers = []
        lines = result.stdout.splitlines()
        for line in lines:
            if "DNS Servers" in line:
                _, dns = line.split(":", 1)
                dns_servers.append(dns.strip())
            elif dns_servers and line.startswith(" "):
                dns_servers.append(line.strip())
        
        if dns_servers:
            # for dns in dns_servers:
            system_primary.value = dns_servers[0]
            system_secondary.value = dns_servers[1]
            page.update()
        else:
            print("هیچ DNS تنظیم شده‌ای پیدا نشد.")

    def submit(e):
        global primary
        primary_local = primary.value
        global secondary
        secondary_local = secondary.value
        if e.control.text == 'پاک کردن':
            primary_local = ''
            secondary_local = ''
        result = subprocess.getstatusoutput(f'wmic nicconfig where (IPEnabled=TRUE) call SetDNSServerSearchOrder ({primary_local},{secondary_local})')
        page.dialog = ft.AlertDialog(
            content=ft.Column([
                ft.Text('dns با موفقیت اعمال شد',text_align=ft.TextAlign.CENTER,rtl=True)
            ])
        )
        page.dialog.rtl = True
        page.dialog.open =True
        get_dns_servers()
        page.update()

    
    def radio_select(e):
        if e.data == '403':
            primary.value = '10.202.10.202'
            secondary.value = '10.202.10.102'
        elif e.data == 'شکن':
            primary.value = '178.22.122.100'
            secondary.value = '185.51.200.2'
        page.update()
    
    get_dns_servers()
    dns_403 = ft.Radio(value='403',label='403')
    dns_shekn = ft.Radio(value='شکن',label='شکن')
    
    mainrow = ft.Row(
        controls=[
            ft.Column(controls=[
                ft.RadioGroup(
                    content=ft.Column([
                        ft.Row([dns_403,ft.IconButton(icon=ft.icons.EDIT)]),
                        ft.Row([dns_shekn,ft.IconButton(icon=ft.icons.EDIT)]),
                        
                    ],
                    ),
                    on_change = radio_select
                )
            ],
            width= w*1/3
            ),
            ft.Column(
                [
                    ft.Row([
                        ft.Text('primary'),
                        primary,
                            ],
                        
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,
                        ),
                    ft.Row([
                        ft.Text('secondary'),
                        secondary,
                        ],
                        
                        alignment=ft.MainAxisAlignment.SPACE_AROUND,


                ),
                ft.Row([ft.ElevatedButton('ثبت',on_click=submit),ft.ElevatedButton('پاک کردن',on_click=submit)])
                ],
                
                width= w*2/3,
                rtl=False,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            ),
        ],
        alignment=ft.MainAxisAlignment.START,
        
    )

    page.update()
    page.add(ft.Column([
        mainrow,
        ft.Divider(10,4,ft.colors.RED),
        ft.Text('مقدار dns های سیستم',text_align=ft.TextAlign.CENTER),
        ft.Column(
                [
                    ft.Row([
                        ft.Text('primary'),
                        system_primary,
                            ],
                        rtl=False,
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER
                        ),
                    ft.Row([
                        ft.Text('secondary'),
                        system_secondary,
                        ],
                        rtl=False,    
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment = ft.CrossAxisAlignment.CENTER 
                ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment= ft.CrossAxisAlignment.CENTER
        )
    ],
    alignment=ft.MainAxisAlignment.CENTER,
    horizontal_alignment= ft.CrossAxisAlignment.CENTER
    )
    )

ft.app(target=main)