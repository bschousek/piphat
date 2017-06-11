
/* Autogenerated by /usr/bin/instcomp on Thu May 11 20:46:13 2017 -- do not edit */

#include "rtapi.h"
#ifdef RTAPI
#include "rtapi_app.h"
#endif
#include "rtapi_string.h"
#include "rtapi_errno.h"
#include "hal.h"
#include "hal_priv.h"
#include "hal_accessor.h"
#include "hal_internal.h"

static int comp_id;


static char *compname = "pp_dout";

#ifdef MODULE_INFO
MODULE_INFO(machinekit, "component:pp_dout:Raspberry PI digital output for Machinekit via pigpio library");
MODULE_INFO(machinekit, "pin:value:bit:None:in::None");
MODULE_INFO(machinekit, "pin:pinmode:u32:None:in::1");
MODULE_INFO(machinekit, "pin:bcm:u32:None:in::None");
MODULE_INFO(machinekit, "pin:pi_instance:u32:None:in::None");
MODULE_INFO(machinekit, "license:GPL");
MODULE_INFO(machinekit, "author:Brian Schousek");
MODULE_INFO(machinekit, "funct:write:1:");
MODULE_LICENSE("GPL");
#endif // MODULE_INFO
RTAPI_TAG(HAL,HC_INSTANTIABLE);


struct inst_data
    {
    hal_bit_t *value;
    hal_u32_t *pinmode;
    hal_u32_t *bcm;
    hal_u32_t *pi_instance;
    int local_argc;
    char **local_argv;
    };

static int maxpins __attribute__((unused)) = 0;
static int write(void *arg, const hal_funct_args_t *fa);

static int instantiate(const int argc, const char**argv);

static int delete(const char *name, void *inst, const int inst_size);

#undef TRUE
#undef FALSE
#undef true
#define true (1)
#undef false
#define false (0)

static int export_halobjs(struct inst_data *ip, int owner_id, const char *name, const int argc, const char **argv)
{
    char buf[HAL_NAME_LEN + 1];
    int r = 0;
    int j __attribute__((unused)) = 0;
    int z __attribute__((unused)) = 0;
    r = hal_pin_bit_newf(HAL_IN, &(ip->value), owner_id,
            "%s.value", name);
    if(r != 0) return r;

    r = hal_pin_u32_newf(HAL_IN, &(ip->pinmode), owner_id,
            "%s.pinmode", name);
    if(r != 0) return r;

    *(ip->pinmode) = 1;
    r = hal_pin_u32_newf(HAL_IN, &(ip->bcm), owner_id,
            "%s.bcm", name);
    if(r != 0) return r;

    r = hal_pin_u32_newf(HAL_IN, &(ip->pi_instance), owner_id,
            "%s.pi-instance", name);
    if(r != 0) return r;


    ip->local_argv = halg_dupargv(1, argc, argv);

    ip->local_argc = argc;


    // exporting an extended thread function:
    hal_export_xfunct_args_t write_xf = 
        {
        .type = FS_XTHREADFUNC,
        .funct.x = write,
        .arg = ip,
        .uses_fp = 1,
        .reentrant = 0,
        .owner_id = owner_id
        };

    rtapi_snprintf(buf, sizeof(buf),"%s.write", name);
    r = hal_export_xfunctf(&write_xf, buf, name);
    if(r != 0)
        return r;
    return 0;
}

// constructor - init all HAL pins, funct etc here
static int instantiate(const int argc, const char**argv)
{
struct inst_data *ip;
// argv[0]: component name
const char *name = argv[1];
int r;

// allocate a named instance, and some HAL memory for the instance data
int inst_id = hal_inst_create(name, comp_id, sizeof(struct inst_data), (void **)&ip);

    if (inst_id < 0)
        return -1;

// here ip is guaranteed to point to a blob of HAL memory of size sizeof(struct inst_data).
    hal_print_msg(RTAPI_MSG_DBG,"%s inst=%s argc=%d",__FUNCTION__, name, argc);

// Debug print of params and values

// These pins - pin_ptrs- functs will be owned by the instance, and can be separately exited with delinst
    r = export_halobjs(ip, inst_id, name, argc, argv);
    return r;
}

int rtapi_app_main(void)
{
    comp_id = hal_xinit(TYPE_RT, 0, 0, instantiate, delete, compname);

    if (comp_id < 0)

        return -1;

    hal_ready(comp_id);

    return 0;
}

void rtapi_app_exit(void)
{
    hal_exit(comp_id);
}

// Custom destructor - delete()
// pins, pin_ptrs, and functs are automatically deallocated regardless if a
// destructor is used or not (see below)
//
// Some objects like vtables, rings, threads are not owned by a component
// interaction with such objects may require a custom destructor for
// cleanup actions
// Also allocated memory that hal_lib will know nothing about ie local_argv
//
// NB: if a customer destructor is used, it is called
// - after the instance's functs have been removed from their respective threads
//   (so a thread funct call cannot interact with the destructor any more)
// - any pins and params of this instance are still intact when the destructor is
//   called, and they are automatically destroyed by the HAL library once the
//   destructor returns


static int delete(const char *name, void *inst, const int inst_size)
{

    struct inst_data *ip = inst;

    HALDBG("Entering delete() : inst=%s size=%d %p local_argv = %p\n", name, inst_size, inst, ip->local_argv);

    HALDBG("Before free ip->local_argv[0] = %s\n", ip->local_argv[0]);

   	halg_free_argv(1, ip->local_argv);

    HALDBG("Now ip->local_argv[0] = %s\n", ip->local_argv[0]);

    return 0;

}


#undef FUNCTION
#define FUNCTION(name) static int name(void *arg, const hal_funct_args_t *fa)
#undef fperiod
#define fperiod (period * 1e-9)
#undef value
#define value (0+*ip->value)
#undef pinmode
#define pinmode (0+*ip->pinmode)
#undef bcm
#define bcm (0+*ip->bcm)
#undef pi_instance
#define pi_instance (0+*ip->pi_instance)
#undef local_argc
#define local_argc (ip->local_argc)
#undef local_argv
#define local_argv(i) (ip->local_argv[i])


#line 20 "pp_dout.icomp"
#include <pigpiod_if2.h>

FUNCTION(write) {
long period __attribute__((unused)) = fa_period(fa);
struct inst_data *ip __attribute__((unused)) = arg;

	set_mode(pi_instance, bcm, pinmode);

	gpio_write(pi_instance, bcm, value);

	return 0;

}




