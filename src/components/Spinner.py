from Component_py.stubs import require, __pragma__  # __:skip
React = require("react")
PropTypes = require("prop-types")
RingLoader = require("react-spinners").RingLoader

def Spinner(props):
    loading = props["loading"]
    if not loading:
        return None

    return __pragma__("xtrans", None, "{}", """ (
        <div className="d-flex justify-content-center align-items-center">
            <RingLoader
                color="#999"
                size={42}
                loading={loading} />
            Loading..
        </div>
    ); """)

Spinner.propTypes = {
    "loading": PropTypes.bool.isRequired
}
